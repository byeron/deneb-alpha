from domain.interface.multipletest import IMultipletest
from domain.interface.multipletest_config import IMultipletestConfig


class Multipletest(IMultipletest):
    def __init__(self, config: IMultipletestConfig):
        if not hasattr(config, "method"):
            raise AttributeError("method is not set")

        if not hasattr(config, "alpha"):
            raise AttributeError("alpha is not set")

        self.method = config.method
        self.alpha = config.alpha

    def run(
        self, pvalues: list[float]
    ) -> list[list[float], list[bool]]:  # P-Values, Rejected
        print("Multipletest.run()")
        print(f"method: {self.method}, alpha: {self.alpha}")
        return [[0.1, 0.2, 0.3], [True, False, True]]
