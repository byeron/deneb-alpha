from dataclasses import dataclass
from typing import Literal

from domain.interface.dissimilarity_config import IDissimilarityConfig


@dataclass(frozen=True)
class DissimilarityConfig(IDissimilarityConfig):
    experiment: str
    corr_method: Literal["pearson", "spearman"]
    dissimilarity: Literal["abslinear"]

    def __post_init__(self):
        if not isinstance(self.experiment, str):
            raise TypeError(f"Invalid type: {type(self.experiment)}")

        if not isinstance(self.corr_method, str):
            raise TypeError(f"Invalid type: {type(self.corr_method)}")

        if not isinstance(self.dissimilarity, str):
            raise TypeError(f"Invalid type: {type(self.dissimilarity)}")

        if self.corr_method not in ["pearson", "spearman"]:
            raise ValueError(f"Invalid corr_method: {self.corr_method}")

        if self.dissimilarity not in ["abslinear"]:
            raise ValueError(f"Invalid dissimilarity: {self.dissimilarity}")