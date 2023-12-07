from dataclasses import dataclass

from domain.interface.clustering_config import IClusteringConfig


@dataclass(frozen=True)
class ClusteringConfig(IClusteringConfig):
    cutoff: float
    rank: int
    method: str
    criterion: str
