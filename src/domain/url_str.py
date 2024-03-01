from dataclasses import dataclass


@dataclass(frozen=True)
class UrlStr:
    value: str
