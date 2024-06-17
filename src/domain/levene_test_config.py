from dataclasses import dataclass

from domain.interface.fluctuation_config import IFluctuationConfig


@dataclass(frozen=True)
class LeveneTestConfig(IFluctuationConfig):
    control: str
    experiment: str
    alpha: float

    def __post_init__(self):
        if self.alpha <= 0 or self.alpha >= 1:
            raise ValueError("Alpha must be between 0 and 1")
        if self.control == self.experiment:
            raise ValueError("Control and experiment must be different")
        if not self.control or not self.experiment:
            raise ValueError("Control and experiment must be non-empty")
        if not isinstance(self.alpha, (int, float)):
            raise ValueError("Alpha must be a number")
        if not isinstance(self.control, str) or not isinstance(self.experiment, str):
            raise ValueError("Control and experiment must be strings")
