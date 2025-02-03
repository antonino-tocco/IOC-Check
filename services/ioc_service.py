
import os
import json
import threading

import requests

from datetime import datetime
from classes import Singleton, singleton
from constants import PULSES_FILE
from models import Pulse
from utils import Logger


@singleton
class IOCService:
    def __init__(self, api_key = None):
        self.pulses = []
        self.api_key = api_key

    def load_iocs(self):
        self.pulses = []
        if not os.path.exists(PULSES_FILE):
            self.retrieve_iocs()
        with open(PULSES_FILE) as f:
            data = json.load(f)
            self.pulses = [Pulse(**x) for x in data["pulses"]]
        return self.pulses

    def retrieve_iocs(self):
        next_url = "https://otx.alienvault.com/api/v1/pulses/subscribed?limit=1000&page=1&format=json"
        if os.path.exists(PULSES_FILE):
            with open(PULSES_FILE) as f:
                data = json.load(f)
                last_updated = datetime.fromisoformat(data["last_updated"])
                Logger.info("IOCs last updated at: {}".format(last_updated))
                if (datetime.now() - last_updated).days < 1:
                    Logger.info("IOCs up to date")
                    return

        while next_url is not None:
            response = self.__retrieve_ioc_page(next_url)
            if response.status_code == 200:
                response_body = response.json()
                self.pulses.extend(Pulse(**x) for x in response_body["results"])
                next_url = response_body["next"]
            else:
                print("Failed to retrieve IOCs {} {}".format(response.status_code, response.text))
        with open(PULSES_FILE, "w") as f:
            json.dump({
                "last_updated": str(datetime.now()),
                "pulses": [x.model_dump() for x in self.pulses]
            }, f)

    def __retrieve_ioc_page(self, url):
        response = requests.get(url, headers={"X-OTX-API-KEY": self.api_key})
        return response
