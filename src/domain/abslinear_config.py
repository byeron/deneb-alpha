from dataclasses import dataclass
from domain.dissimilarity_config import DissimilarityConfig


@dataclass(frozen=True)
class AbsLinearConfig(DissimilarityConfig):
    def __post_init__(self):
        super().__post_init__()
