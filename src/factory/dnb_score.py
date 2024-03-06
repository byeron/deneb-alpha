from injector import Module

from domain.abslinear_config import AbsLinearConfig
from domain.clustering_config import ClusteringConfig
from domain.ftest_config import FtestConfig
from domain.interface.clustering import IClustering
from domain.interface.dissimilarity import IDissimilarity
from domain.interface.dnb_score import IDNBScore
from domain.interface.fluctuation import IFluctuation
from domain.interface.multiple_correction import IMultipleCorrection
from domain.multipletest_config import MultipletestConfig
from usecase.abslinear import AbsLinear
from usecase.clustering import Clustering
from usecase.dnb_score import DNBScore
from usecase.ftest import Ftest
from usecase.multipletest import Multipletest


class DNBScoreFactory(Module):
    def __init__(
        self,
        control,
        experiment,
        alpha,
        is_apply_multiple_correction,
        multiple_correction_method,
        corr_method,
        dissimilarity_metric,
        cutoff,
        rank,
        linkage_method,
        criterion,
    ):
        self.alpha = alpha
        self.control = control
        self.experiment = experiment
        self.is_apply_multiple_correction = is_apply_multiple_correction
        self.multiple_correction_method = multiple_correction_method
        self.corr_method = corr_method
        self.dissimilarity_metric = dissimilarity_metric
        self.cutoff = cutoff
        self.rank = rank
        self.linkage_method = linkage_method
        self.criterion = criterion

    def fluctuation_factory(self):
        config = FtestConfig(
            control=self.control,
            experiment=self.experiment,
            alpha=self.alpha,
        )
        return Ftest(config)

    def correction_factory(self):
        config = MultipletestConfig(
            self.multiple_correction_method,
            self.alpha,
            self.is_apply_multiple_correction,
        )
        return Multipletest(config)

    def dissimilarity_factory(self):
        match self.dissimilarity_metric:
            case "abslinear":
                config = AbsLinearConfig(
                    self.experiment, self.corr_method, self.dissimilarity_metric
                )
                return AbsLinear(config)

    def clustering_factory(self):
        config = ClusteringConfig(
            self.cutoff,
            self.rank,
            self.linkage_method,
            self.criterion,
        )
        return Clustering(config)

    def configure(self, binder):
        binder.bind(IClustering, to=self.clustering_factory())
        binder.bind(IDissimilarity, to=self.dissimilarity_factory())
        binder.bind(IMultipleCorrection, to=self.correction_factory())
        binder.bind(IFluctuation, to=self.fluctuation_factory())
        binder.bind(IDNBScore, to=DNBScore)
