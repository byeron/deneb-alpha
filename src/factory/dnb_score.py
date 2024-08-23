from injector import Injector, Module

from domain.interface.clustering import IClustering
from domain.interface.dissimilarity import IDissimilarity
from domain.interface.dnb_score import IDNBScore
from domain.interface.fluctuation import IFluctuation
from domain.interface.multiple_correction import IMultipleCorrection
from factory.clustering import ClusteringFactory
from factory.correction import CorrectionFactory
from factory.dissimilarity import DissimilarityFactory
from factory.fluctuation import FluctuationFactory
from usecase.dnb_score import DNBScore


class DNBScoreFactory(Module):
    def __init__(
        self,
        experiment: str = None,
        fluctuation_method: str = None,
        fluctuation_threshold: float = None,
        fluctuation_alpha: float = None,
        is_apply_multiple_correction: bool = None,
        multiple_correction_method: str = None,
        corr_method: str = None,
        dissimilarity_metric: str = None,
        cutoff: float = None,
        rank: int = None,
        linkage_method: str = None,
        criterion: str = None,
        control: str = None,
    ):
        factory = FluctuationFactory(
            control=control,
            experiment=experiment,
            method=fluctuation_method,
            threshold=fluctuation_threshold,
            alpha=fluctuation_alpha,
        )
        injector = Injector(factory.configure)
        self.fluctuation_handler = injector.get(IFluctuation)

        factory = CorrectionFactory(
            method=multiple_correction_method,
            alpha=fluctuation_alpha,
            apply=is_apply_multiple_correction,
        )
        injector = Injector(factory.configure)
        self.correction_handler = injector.get(IMultipleCorrection)

        factory = DissimilarityFactory(
            experiment=experiment,
            corr_method=corr_method,
            dissimilarity=dissimilarity_metric,
        )
        injector = Injector(factory.configure)
        self.dissimilarity_handler = injector.get(IDissimilarity)

        factory = ClusteringFactory(
            cutoff=cutoff,
            rank=rank,
            linkage_method=linkage_method,
            criterion=criterion,
        )
        injector = Injector(factory.configure)
        self.clustering_handler = injector.get(IClustering)

    def configure(self, binder):
        binder.bind(
            IDNBScore,
            to=DNBScore(
                self.fluctuation_handler,
                self.correction_handler,
                self.dissimilarity_handler,
                self.clustering_handler,
            ),
        )
