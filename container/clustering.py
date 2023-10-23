from dependency_injector import containers, providers

from domain.clustering_config import ClusteringConfig
from usecase.clustering import Clustering


class ClusteringContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    clustering_config = providers.Factory(
        ClusteringConfig,
        cutoff=config.cutoff,
        rank=config.rank,
        method=config.method,
        criterion=config.criterion,
    )
    handler = providers.Factory(Clustering, clustering_config=clustering_config)
