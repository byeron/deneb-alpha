from injector import inject
from statsmodels.stats.multitest import multipletests

from domain.interface.multipletest import IMultipletest
from domain.interface.multipletest_config import IMultipletestConfig


class Multipletest(IMultipletest):
    @inject
    def __init__(self, config: IMultipletestConfig):
        if not hasattr(config, "method"):
            raise AttributeError("method is not set")

        if not hasattr(config, "alpha"):
            raise AttributeError("alpha is not set")

        self.method = config.method
        self.alpha = config.alpha

    def run(
        self, pvalues: list[float]
    ) -> tuple[list[float], list[bool]]:  # P-Values, Rejected
        reject, pvals_corrected, _, _ = multipletests(
            pvalues, alpha=self.alpha, method=self.method
        )
        # cast to primitive data type
        reject = [bool(r) for r in reject]
        pvals_corrected = [float(p) for p in pvals_corrected]
        return (pvals_corrected, reject)
