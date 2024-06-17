from injector import Module

from domain.ftest_config import FtestConfig
from domain.interface.fluctuation import IFluctuation
from domain.mad_ratio_config import MadRatioConfig
from usecase.ftest import Ftest
from usecase.mad_ratio import MADRatio


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
            case _:
                raise ValueError("method is not supported")

    def factory(self):
        match self.method:
            case "ftest":
                return Ftest(self.config)
            case "mad-ratio":
                return MADRatio(self.config)
            case _:
                raise ValueError

    def configure(self, binder):
        binder.bind(IFluctuation, to=self.factory())
