from injector import Module

from domain.ftest_config import FtestConfig
from domain.interface.fluctuation import IFluctuation
from domain.mad_ratio_config import MadRatioConfig
from usecase.ftest import Ftest
from usecase.mad_ratio import MADRatio
from domain.mad_ftest_config import MADFtestConfig
from usecase.mad_ftest import MADFtest


class FluctuationFactory(Module):
    def __init__(self, control, experiment, method, alpha=None, mad_threshold=None):
        self.method = method
        match method:
            case "ftest":
                if alpha is None:
                    raise ValueError("alpha is required for ftest method")
                self.config = FtestConfig(
                    control=control,
                    experiment=experiment,
                    alpha=alpha,
                )
            case "mad-ratio":
                if mad_threshold is None:
                    raise ValueError("mad_threshold is required for mad method")
                self.config = MadRatioConfig(
                    control=control,
                    experiment=experiment,
                    threshold=mad_threshold,
                )
                print(self.config)
            case "mad-ftest":
                if alpha is None:
                    raise ValueError("alpha is required for ftest method")
                self.config = MADFtestConfig(
                    control=control,
                    experiment=experiment,
                    alpha=alpha,
                )
            case _:
                raise ValueError("method is not supported")

    def factory(self):
        match self.method:
            case "ftest":
                return Ftest(self.config)
            case "mad-ratio":
                return MADRatio(self.config)
            case "mad-ftest":
                return MADFtest(self.config)
            case _:
                raise ValueError("method is not supported in factory")

    def configure(self, binder):
        binder.bind(IFluctuation, to=self.factory())
