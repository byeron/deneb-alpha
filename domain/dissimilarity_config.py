from dataclasses import dataclass

from domain.interface.dissimilarity_config import IDissimilarityConfig


@dataclass(frozen=True)
class DissimilarityConfig(IDissimilarityConfig):
    experiment: str
    corr_method: str
    dissimilarity: str
