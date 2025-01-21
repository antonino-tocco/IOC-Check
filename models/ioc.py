from dataclasses import dataclass
from pydantic import BaseModel


class IOC(BaseModel):
    id: int
    indicator: str
    type: str
    is_active: bool

    def is_file_indicator(self):
        return self.type in ["FileHash-MD5", "FileHash-SHA1", "FileHash-SHA256"]