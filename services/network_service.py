import scapy.all as scapy
from scapy.layers.http import HTTPRequest, HTTPResponse
from classes import singleton
from utils import Logger

from . import IOCService
from .check_service import CheckService


@singleton
class NetworkService(CheckService):
    def __init__(self):
        self.pulses = []

    async def check(self):
        self.pulses = IOCService().load_iocs()
        Logger.info("NetworkService: checking network traffic")
        if not self.pulses or len(self.pulses) == 0:
            Logger.error("NetworkService: no pulses loaded")
            return

        scapy.sniff(prn=self.process_packet, store=False)


    def process_packet(self, packet):
        compromised = False
        if packet.haslayer(HTTPRequest) or packet.haslayer(HTTPResponse):
            host = packet[HTTPRequest].Host if packet.haslayer(HTTPRequest) else packet[HTTPResponse].Host
            Logger.info("NetworkService inspecting http packet with host {}".format(host))

            for pulse in self.pulses:
                ioc_list = list(filter(lambda x: x.is_network_indicator(), pulse.indicators))
                compromised = compromised or host in [x.indicator for x in ioc_list]

            if compromised:
                Logger.info("NetworkService http communication with host compromised {}".format(host))

        if packet.haslayer(scapy.IP):
            src = packet[scapy.IP].src
            dst = packet[scapy.IP].dst
            Logger.info("NetworkService inspecting ip packet with src {} dst {}".format(src, dst))
            for pulse in self.pulses:
                ioc_list = list(filter(lambda x: x.is_network_indicator(), pulse.indicators))
                compromised = compromised or any([x.indicator in src or x.indicator in dst for x in ioc_list])

            if compromised:
                Logger.info("NetworkService ip communication with src {} dst {} compromised".format(src, dst))