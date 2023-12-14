from dataclasses import dataclass
from typing import Literal

from domain.interface.clustering_config import IClusteringConfig


@dataclass(frozen=True)
class ClusteringConfig(IClusteringConfig):
    cutoff: float
    rank: int
    method: Literal[
        "single", "complete", "average", "weighted", "centroid", "median", "ward"
    ]
    criterion: Literal["inconsistent", "distance", "maxclust"]

    def __post_init__(self):
        if not isinstance(self.cutoff, float):
            raise TypeError("cutoff must be float type")

        if not isinstance(self.rank, int):
            raise TypeError("rank must be int type")

        if not isinstance(self.method, str):
            raise TypeError("method must be str type")

        if not isinstance(self.criterion, str):
            raise TypeError("criterion must be str type")

        if not 0 < self.cutoff < 1:
            raise ValueError("cutoff must be between 0 and 1")

        if not 0 < self.rank:
            raise ValueError("rank must be greater than 0")

        if self.method not in [
            "single",
            "complete",
            "average",
            "weighted",
            "centroid",
            "median",
            "ward",
        ]:
            raise ValueError(
                "method must be one of single, complete, average, weighted, centroid, median, ward"
            )

        if self.criterion not in ["inconsistent", "distance", "maxclust"]:
            raise ValueError(
                "criterion must be one of inconsistent, distance, maxclust"
            )
