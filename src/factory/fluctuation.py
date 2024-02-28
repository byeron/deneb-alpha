from injector import Module

from domain.ftest_config import FtestConfig
from domain.interface.fluctuation import IFluctuation
from usecase.ftest import Ftest


class FluctuationFactory(Module):
    def __init__(self, control, experiment, alpha):
        self.config = FtestConfig(
            control=control,
            experiment=experiment,
            alpha=alpha,
        )

    def factory(self):
        # Future plan
        """
        match self.config.method:
            case hoge:
                return Hoge()
            case _:
                raise ValueError
        """
        return Ftest(self.config)

    def configure(self, binder):
        binder.bind(IFluctuation, to=self.factory())
