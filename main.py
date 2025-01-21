import asyncio
from argparse import ArgumentParser

from services import IOCService
from services.file_system_service import FileSystemService


def __run_file_system_service(file_system_service: FileSystemService):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(file_system_service.check())


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--otx_api_key', type=str, default=None, required=True)
    parser.add_argument('--vt_api_key', type=str, default=None)
    parser.add_argument('--base_path', type=str, default=None)
    args = parser.parse_args()

    if args.otx_api_key:
        ioc_service = IOCService(args.otx_api_key)
        ioc_service.load_iocs()
    file_system_service = FileSystemService(vt_api_key=args.vt_api_key, base_path=args.base_path)
    __run_file_system_service(file_system_service)