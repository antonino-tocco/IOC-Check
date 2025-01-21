import requests

from classes import singleton
from services.check_service import CheckService


@singleton
class VTService(CheckService):

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3"

    def check(self, hash):
        response = requests.get(f"{self.base_url}/files/{hash}", headers={"X-ApiKey": self.api_key})
        if response.status_code == 200:
            data = response.json()["data"]
            return data["attributes"]["last_analysis_stats"]
        else:
            return None

