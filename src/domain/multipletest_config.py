from dataclasses import dataclass

from domain.interface.multipletest_config import IMultipletestConfig


@dataclass(frozen=True)
class MultipletestConfig(IMultipletestConfig):
    method: str
    alpha: float
