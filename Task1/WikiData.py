from dataclasses import dataclass


@dataclass
class WikiData:
    website: str
    popularity: int
    frontend: str
    backend: str