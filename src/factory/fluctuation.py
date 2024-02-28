from usecase.ftest import Ftest
from domain.ftest_config import FtestConfig
from injector import Module
from domain.interface.fluctuation import IFluctuation


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
