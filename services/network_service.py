from classes import singleton
from .check_service import CheckService


@singleton
class NetworkService(CheckService):
    def check(self):
        print("NetworkService: check method called")
        return True