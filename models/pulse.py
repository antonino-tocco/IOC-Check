from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict
from typing import Optional

from .ioc import IOC


class Pulse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    description: str
    author_name: str
    tags: list[str]
    adversary: Optional[str]
    public: int
    tlp: Optional[str]
    targeted_countries: list[str]
    malware_families: list[str]
    indicators: list[IOC]
    attack_ids: list[str]
    references: list[str]
    industries: list[str]
    extract_source: list[str]
    more_indicators: bool