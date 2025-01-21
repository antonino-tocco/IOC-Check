from pydantic import BaseModel, ConfigDict, Field

def to_snake_case(name: str) -> str:
    return "_".join(name.split("-")).lower()

class Stat(BaseModel):
    model_config = ConfigDict(extra="ignore", alias_generator=to_snake_case)
    malicious: int
    suspicious: int
    undetected: int
    harmless: int
    timeout: int
    confirmed_timeout: int = Field(alias="confirmed-timeout")
    failure: int
    type_unsupported: int = Field(alias="type-unsupported")