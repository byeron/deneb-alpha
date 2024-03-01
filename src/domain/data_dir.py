from dataclasses import dataclass


@dataclass(frozen=True)
class DataDir:
    value: str
