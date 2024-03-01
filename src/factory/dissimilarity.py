from injector import Module
from domain.interface.dissimilarity_config import IDissimilarityConfig
from domain.dissimilarity_config import DissimilarityConfig
from domain.interface.dissimilarity import IDissimilarity
from usecase.abslinear import AbsLinear


class DissimilarityFactory(Module):
    def __init__(self, experiment, corr_method, dissimilarity):
        self.experiment = experiment
        self.corr_method = corr_method
        self.dissimilarity = dissimilarity

    def configure(self, binder):
        match self.dissimilarity:
            case "abslinear":
                binder.bind(
                    IDissimilarityConfig,
                    to=DissimilarityConfig(
                        self.experiment,
                        self.corr_method,
                        self.dissimilarity,
                    )
                )
                binder.bind(IDissimilarity, to=AbsLinear)
            case _:
                raise ValueError
