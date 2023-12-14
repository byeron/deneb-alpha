from dataclasses import dataclass

from domain.interface.fluctuation_config import IFluctuationConfig


@dataclass(frozen=True)
class FtestConfig(IFluctuationConfig):
    control: str
    experiment: str
    alpha: float

    def __post_init__(self):
        # validate control
        if not isinstance(self.control, str):
            raise TypeError(f"control must be str: {self.control}")

        # validate experiment
        if not isinstance(self.experiment, str):
            raise TypeError(f"experiment must be str: {self.experiment}")

        # validate alpha
        if not isinstance(self.alpha, float):
            raise TypeError(f"alpha must be float: {self.alpha}")

        if self.alpha <= 0 or self.alpha >= 1:
            raise ValueError(f"alpha must be in (0, 1): {self.alpha}")