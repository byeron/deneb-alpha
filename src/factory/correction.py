from domain.multipletest_config import MultipletestConfig
from domain.interface.multipletest_config import IMultipletestConfig
from usecase.multipletest import Multipletest
from domain.interface.multipletest import IMultipletest
from injector import Module


class CorrectionFactory(Module):
    def __init__(self, method: str, alpha: float):
        self.method = method
        self.alpha = alpha

    def configure(self, binder):
        binder.bind(IMultipletestConfig, to=MultipletestConfig(self.method, self.alpha))
        binder.bind(IMultipletest, to=Multipletest)
