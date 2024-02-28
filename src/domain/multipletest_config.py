from dataclasses import dataclass
from typing import Literal

from domain.interface.multipletest_config import IMultipletestConfig
from injector import inject


@inject
@dataclass(frozen=True)
class MultipletestConfig(IMultipletestConfig):
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

    def __post_init__(self):
        if not isinstance(self.method, str):
            raise TypeError("method must be str type")

        if not isinstance(self.alpha, float):
            raise TypeError("alpha must be float type")

        if not 0 < self.alpha < 1:
            raise ValueError("alpha must be between 0 and 1")
