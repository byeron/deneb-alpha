from dependency_injector import containers, providers

from domain.dissimilarity_config import DissimilarityConfig
from usecase.abslinear import AbsLinear


class AbsLinearContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    dissimilarity_config = providers.Factory(
        DissimilarityConfig,
        experiment=config.experiment,
        corr_method=config.corr_method,
        dissimilarity=config.dissimilarity,
    )
    handler = providers.Factory(AbsLinear, dissimilarity_config=dissimilarity_config)
