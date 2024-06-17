from dataclasses import dataclass

from domain.interface.fluctuation_config import IFluctuationConfig


@dataclass(frozen=True)
class MADFtestConfig(IFluctuationConfig):
    control: str
    experiment: str
    alpha: float

    def __post_init__(self):
        if self.alpha <= 0 or self.alpha >= 1:
            raise ValueError("alpha must be in (0, 1)")
        if self.control == self.experiment:
            raise ValueError("control and experiment must be different")
        if not self.control or not self.experiment:
            raise ValueError("control and experiment must be non-empty")
        if not isinstance(self.alpha, float):
            raise ValueError("alpha must be float")
        if not isinstance(self.control, str) or not isinstance(self.experiment, str):
            raise ValueError("control and experiment must be str")
