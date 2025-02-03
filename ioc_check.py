import argparse
import asyncio
from argparse import ArgumentParser

from services import IOCService, FileSystemService, NetworkService


def __run_file_system_service(file_system_service: FileSystemService):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(file_system_service.check())

def __run_network_service(network_service: NetworkService):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(network_service.check())


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--file_system', action='store_true', default=False)
    parser.add_argument('--otx_api_key', type=str, default=None)
    parser.add_argument('--vt_api_key', type=str, default=None)
    parser.add_argument('--base_path', type=str, default=None)
    parser.add_argument('--network', action='store_true', default=False)
    #parser.add_argument('--file', type=str, default=None)
    args = parser.parse_args()

    if args.otx_api_key:
        ioc_service = IOCService(args.otx_api_key)
        ioc_service.retrieve_iocs()

    if args.file_system:
        file_system_service = FileSystemService(vt_api_key=args.vt_api_key, base_path=args.base_path)
        __run_file_system_service(file_system_service)

    if args.network:
        network_service = NetworkService()
        __run_network_service(network_service)