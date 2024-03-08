from dataclasses import dataclass
from typing import Literal

from injector import inject

from domain.interface.multiple_correction_config import \
    IMultipleCorrectionConfig


@inject
@dataclass(frozen=True)
class MultipletestConfig(IMultipleCorrectionConfig):
    method: Literal[
        "bonferroni",
        "sidak",
        "holm-sidak",
        "holm",
        "simes-hochberg",
        "hommel",
        "fdr_bh",
        "fdr_by",
        "fdr_tsbh",
        "fdr_tsbky",
    ]
    alpha: float
    apply: bool

    def __post_init__(self):
        if not isinstance(self.method, str):
            raise TypeError("method must be str type")

        if not isinstance(self.alpha, float):
            raise TypeError("alpha must be float type")

        if not 0 < self.alpha < 1:
            raise ValueError("alpha must be between 0 and 1")
