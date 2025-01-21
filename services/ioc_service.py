import json
import os
import threading

import requests

from classes import Singleton, singleton
from models import Pulse

@singleton
class IOCService:
    def __init__(self, api_key = None):
        self.pulses = []
        self.api_key = api_key

    def load_iocs(self):
        self.pulses = []
        if not os.path.exists("pulses.json"):
            self.retrieve_iocs()
        with open("pulses.json") as f:
            self.pulses = [Pulse(**x) for x in json.load(f)]
        return self.pulses

    def retrieve_iocs(self):
        next_url = "https://otx.alienvault.com/api/v1/pulses/subscribed?limit=1000&page=1&format=json"
        while next_url is not None:
            response = self.__retrieve_ioc_page(next_url)
            if response.status_code == 200:
                response_body = response.json()
                self.pulses.extend(Pulse(**x) for x in response_body["results"])
                next_url = response_body["next"]
            else:
                print("Failed to retrieve IOCs {} {}".format(response.status_code, response.text))
        with open("pulses.json", "w") as f:
            json.dump(list(map(lambda x: x.model_dump(), self.pulses)), f)

    def __retrieve_ioc_page(self, url):
        response = requests.get(url, headers={"X-OTX-API-KEY": self.api_key})
        return response
