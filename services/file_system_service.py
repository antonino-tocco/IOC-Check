import os
import ctypes
import hashlib

from binaryornot.check import is_binary

from classes import Singleton, singleton
from models import Stat
from utils.logger import Logger
from . import IOCService

from .check_service import CheckService
from .vt_service import VTService

indicator_type_to_hash = {
    "FileHash-MD5": hashlib.md5,
    "FileHash-SHA1": hashlib.sha1,
    "FileHash-SHA256": hashlib.sha256
}

@singleton
class FileSystemService(CheckService):
    def __init__(self, vt_api_key=None, base_path=None):
        super().__init__()
        self.vt_client = None
        if base_path is not None:
            self.base_path = base_path
        else:
            self.base_path = os.path.join(os.environ['USERPROFILE'], "")
        if vt_api_key is not None:
            self.vt_client = VTService(vt_api_key)
        print("FileSystemService: base_path: {}".format(self.base_path))

    async def check(self, base_path=None):
        self.pulses = IOCService().load_iocs()
        files = self.__recursive_walk(base_path if base_path is not None else self.base_path)
        for file in files:
            await self.__inspect_file(file)

    async def __inspect_file(self, file: str):
        """Inspect a file for IOCs"""
        if not os.path.exists(file):
            return
        Logger().info("FileSystemService: inspecting file {}".format(file))
        content = None
        try:
            open_mode = "rb" if is_binary(file) else "r"
            with open(file, open_mode) as f:
                content = f.read()
                if open_mode != "rb":
                    content = content.encode()
        except FileNotFoundError as e:
            Logger().error("FileSystemService: file not found {}".format(file))
            return
        except PermissionError as e:
            Logger().error("FileSystemService: permission denied {}".format(file))
            return
        except Exception as e:
            Logger().error("FileSystemService: error while opening file {}".format(e))
            return
        stat = await self.__vt_inpection(file=file, content=content)
        if stat is not None:
            Logger().info("FileSystemService: found file {} in VT".format(file))
            Logger().info(stat)
        for pulse in self.pulses:
            ioc_list = list(filter(lambda x: x.is_active and x.is_file_indicator(), pulse.indicators))
            for ioc in ioc_list:
                if ioc.type in indicator_type_to_hash:
                    hash = indicator_type_to_hash[ioc.type](content).hexdigest()
                    if ioc.indicator in hash:
                        Logger().info("FileSystemService: found IOC {} in file {} pulse {}".format(ioc.indicator, file, pulse.name))

    async def __vt_inpection(self, file, content: bytes):
        if self.vt_client is not None:
            file_hashes = [hashlib.md5(content).hexdigest(), hashlib.sha1(content).hexdigest(),
                           hashlib.sha256(content).hexdigest()]
            for hash in file_hashes:
                try:
                    result = self.vt_client.check(hash)
                    if result is not None:
                        stat = Stat(**result)
                        return stat
                except vt.error.APIError as e:
                    Logger().error("FileSystemService: error while querying VT {}".format(e))
                except Exception as e:
                    Logger().error("FileSystemService: error while querying VT {}".format(e))

    def __recursive_walk(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                yield os.path.join(root, file)
            for dir in dirs:
                yield from self.__recursive_walk(os.path.join(root, dir))