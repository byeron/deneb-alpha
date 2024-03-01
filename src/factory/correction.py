from injector import Module

from domain.interface.multiple_correction import IMultipleCorrection
from domain.interface.multiple_correction_config import IMultipleCorrectionConfig
from domain.multipletest_config import MultipletestConfig
from usecase.multipletest import Multipletest


class CorrectionFactory(Module):
    def __init__(self, method: str, alpha: float):
        self.method = method
        self.alpha = alpha

    def configure(self, binder):
        binder.bind(IMultipleCorrectionConfig, to=MultipletestConfig(self.method, self.alpha))
        binder.bind(IMultipleCorrection, to=Multipletest)
