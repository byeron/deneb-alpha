from injector import Module

from domain.abslinear_config import AbsLinearConfig
from domain.dissimilarity_metric import DissimilarityMetric
from domain.interface.dissimilarity import IDissimilarity
from domain.interface.dissimilarity_config import IDissimilarityConfig
from usecase.abslinear import AbsLinear


class DissimilarityFactory(Module):
    def __init__(self, experiment, corr_method, dissimilarity):
        self.experiment = experiment
        self.corr_method = corr_method
        self.dissimilarity = dissimilarity

    def configure(self, binder):
        match self.dissimilarity:
            case DissimilarityMetric.abslinear:
                binder.bind(
                    IDissimilarityConfig,
                    to=AbsLinearConfig(
                        self.experiment,
                        self.corr_method,
                        self.dissimilarity,
                    ),
                )
                binder.bind(IDissimilarity, to=AbsLinear)
            case _:
                raise ValueError
