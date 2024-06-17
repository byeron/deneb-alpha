from dataclasses import dataclass

from domain.interface.fluctuation_config import IFluctuationConfig


@dataclass(frozen=True)
class MadRatioConfig(IFluctuationConfig):
    control: str
    experiment: str
    threshold: float

    def __post_init__(self):
        if not isinstance(self.control, str):
            raise TypeError("control must be a string")
        if not isinstance(self.experiment, str):
            raise TypeError("experiment must be a string")
        if not isinstance(self.threshold, float):
            raise TypeError("threshold must be a float")

        if 0 > self.threshold:
            raise ValueError("threshold must be a positive float")
