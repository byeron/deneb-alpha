from dataclasses import dataclass

from domain.interface.fluctuation_config import IFluctuationConfig
from domain.interface.multipletest_config import IMultipletestConfig


@dataclass(frozen=True)
class FtestConfig(IFluctuationConfig):
    control: str
    experiment: str
    alpha: float
