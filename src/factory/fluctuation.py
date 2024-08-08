from injector import Module

from domain.ftest_config import FtestConfig
from domain.interface.fluctuation import IFluctuation
from domain.levene_test_config import LeveneTestConfig
from domain.mad_ftest_config import MadFtestConfig
from domain.mad_ratio_config import MadRatioConfig
from usecase.ftest import Ftest
from usecase.levene_test import LeveneTest
from usecase.mad_ftest import MadFtest
from usecase.mad_ratio import MadRatio
from usecase.std_ratio import StdRatio
from usecase.std_inner_var import StdInnerVar
from domain.std_inner_var_config import StdInnerVarConfig
from usecase.mad_inner_var import MadInnerVar
from domain.mad_inner_var_config import MadInnerVarConfig
from domain.std_ratio_config import StdRatioConfig


class FluctuationFactory(Module):
    def __init__(self, method, experiment, control=None, alpha=None, threshold=None):
        self.method = method
        match method:
            case "ftest":
                if alpha is None:
                    raise ValueError("alpha is required")
                self.config = FtestConfig(
                    control=control,
                    experiment=experiment,
                    alpha=alpha,
                )
            case "mad-ftest":
                if alpha is None:
                    raise ValueError("alpha is required")
                self.config = MadFtestConfig(
                    control=control,
                    experiment=experiment,
                    alpha=alpha,
                )
            case "std-ratio":
                if threshold is None:
                    raise ValueError("threshold is required")
                self.config = StdRatioConfig(
                    control=control,
                    experiment=experiment,
                    threshold=threshold,
                )
            case "mad-ratio":
                if threshold is None:
                    raise ValueError("mad_threshold is required")
                self.config = MadRatioConfig(
                    control=control,
                    experiment=experiment,
                    threshold=threshold,
                )
                print(self.config)
            case "levene":
                if alpha is None:
                    raise ValueError("alpha is required")
                self.config = LeveneTestConfig(
                    control=control,
                    experiment=experiment,
                    alpha=alpha,
                )
            case "std-inner-var":
                if threshold is None:
                    raise ValueError("threshold is required")
                self.config = StdInnerVarConfig(
                    experiment=experiment,
                    threshold=threshold,
                )
            case "mad-inner-var":
                if threshold is None:
                    raise ValueError("threshold is required")
                self.config = MadInnerVarConfig(
                    experiment=experiment,
                    threshold=threshold,
                )
            case _:
                raise ValueError("method is not supported")

    def factory(self):
        match self.method:
            case "ftest":
                return Ftest(self.config)
            case "mad-ftest":
                return MadFtest(self.config)
            case "std-ratio":
                return StdRatio(self.config)
            case "mad-ratio":
                return MadRatio(self.config)
            case "levene":
                return LeveneTest(self.config)
            case "std-inner-var":
                return StdInnerVar(self.config)
            case "mad-inner-var":
                return MadInnerVar(self.config)
            case _:
                raise ValueError("method is not supported in factory")

    def configure(self, binder):
        binder.bind(IFluctuation, to=self.factory())
