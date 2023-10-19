from dataclasses import dataclass

from domain.interface.fluctuation_config import IFluctuationConfig


@dataclass(frozen=True)
class FtestConfig(IFluctuationConfig):
    control: str
    experiment: str
    alpha: float
