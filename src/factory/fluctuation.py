from injector import Module

from domain.fluctuation_method import FluctuationMethod
from domain.ftest_config import FtestConfig
from domain.interface.fluctuation import IFluctuation
from domain.levene_test_config import LeveneTestConfig
from domain.mad_ftest_config import MadFtestConfig
from domain.mad_inner_var_config import MadInnerVarConfig
from domain.mad_ratio_config import MadRatioConfig
from domain.std_inner_var_config import StdInnerVarConfig
from domain.std_ratio_config import StdRatioConfig
from usecase.ftest import Ftest
from usecase.levene_test import LeveneTest
from usecase.mad_ftest import MadFtest
from usecase.mad_inner_var import MadInnerVar
from usecase.mad_ratio import MadRatio
from usecase.std_inner_var import StdInnerVar
from usecase.std_ratio import StdRatio


class FluctuationFactory(Module):
    def __init__(self, method, experiment, control=None, alpha=None, threshold=None):
        self.method = method
        match method:
            case FluctuationMethod.ftest:
                if alpha is None:
                    raise ValueError("alpha is required")
                self.config = FtestConfig(
                    control=control,
                    experiment=experiment,
                    alpha=alpha,
                )
            case FluctuationMethod.mad_ftest:
                if alpha is None:
                    raise ValueError("alpha is required")
                self.config = MadFtestConfig(
                    control=control,
                    experiment=experiment,
                    alpha=alpha,
                )
            case FluctuationMethod.std_ratio:
                if threshold is None:
                    raise ValueError("threshold is required")
                self.config = StdRatioConfig(
                    control=control,
                    experiment=experiment,
                    threshold=threshold,
                )
            case FluctuationMethod.mad_ratio:
                if threshold is None:
                    raise ValueError("mad_threshold is required")
                self.config = MadRatioConfig(
                    control=control,
                    experiment=experiment,
                    threshold=threshold,
                )
                print(self.config)
            case FluctuationMethod.levene:
                if alpha is None:
                    raise ValueError("alpha is required")
                self.config = LeveneTestConfig(
                    control=control,
                    experiment=experiment,
                    alpha=alpha,
                )
            case FluctuationMethod.std_inner_var:
                if control is not None:
                    raise ValueError("control is not required")

                if threshold is None:
                    raise ValueError("threshold is required")
                self.config = StdInnerVarConfig(
                    experiment=experiment,
                    threshold=threshold,
                )
            case FluctuationMethod.mad_inner_var:
                if control is not None:
                    raise ValueError("control is not required")

                if threshold is None:
                    raise ValueError("threshold is required")
                self.config = MadInnerVarConfig(
                    experiment=experiment,
                    threshold=threshold,
                )
            case _:
                raise ValueError(f"method: {method}  is not supported")

    def factory(self):
        match self.method:
            case FluctuationMethod.ftest:
                return Ftest(self.config)
            case FluctuationMethod.mad_ftest:
                return MadFtest(self.config)
            case FluctuationMethod.std_ratio:
                return StdRatio(self.config)
            case FluctuationMethod.mad_ratio:
                return MadRatio(self.config)
            case FluctuationMethod.levene:
                return LeveneTest(self.config)
            case FluctuationMethod.std_inner_var:
                return StdInnerVar(self.config)
            case FluctuationMethod.mad_inner_var:
                return MadInnerVar(self.config)
            case _:
                raise ValueError("method is not supported in factory")

    def configure(self, binder):
        binder.bind(IFluctuation, to=self.factory())
