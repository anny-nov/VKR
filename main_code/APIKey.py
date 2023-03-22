from dataclasses import dataclass


@dataclass
class APIKey:
    id: int
    name: str
    api_key: str
    type: str
    security_descriptor: str