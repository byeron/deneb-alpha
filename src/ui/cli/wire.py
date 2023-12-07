import sys
from enum import Enum, auto

from container.fluctuation import FtestContainer, MultipletestContiner
from container.get_file import GetFileContainer


class FluctuationMethod(Enum):
    FTEST = auto()


class WireFluctuation:
    def __init__(
        self,
        control: str,
        experiment: str,
        fluctuation_method: FluctuationMethod,
        alpha: float,
        multipletest: bool,
        multipletest_method: str,
    ):
        # Set default values
        self._get_file_handler = None
        self._fluctuation_handler = None
        self._multipletest_handler = None

        match fluctuation_method:
            case FluctuationMethod.FTEST:
                container = FtestContainer()
                container.config.from_dict(
                    {
                        "control": control,
                        "experiment": experiment,
                        "alpha": alpha,
                    }
                )
                container.wire(modules=[sys.modules[__name__]])
                self.fluctuation_handler = container.fluctuation_handler()

            case _:
                raise ValueError(f"Invalid method: {multipletest_method}")

        # Setup Handlers
        self.setup_common_handler(alpha, multipletest, multipletest_method)

    def setup_common_handler(self, alpha: float, multipletest: bool, method: str):
        # Setup Handlers
        container = GetFileContainer()
        container.config.from_yaml("./src/config.yml")
        container.wire(modules=[sys.modules[__name__]])
        self.get_file_handler = container.handler()

        # Setup MultipletestHandler
        if multipletest:
            container = MultipletestContiner()
            container.config.from_dict(
                {
                    "method": method,  # "fdr_bh"
                    "alpha": alpha,
                }
            )
            container.wire(modules=[sys.modules[__name__]])
            self.multipletest_handler = container.multipletest_handler()

    @property
    def get_file_handler(self):
        return self._get_file_handler

    @get_file_handler.setter
    def get_file_handler(self, handler):
        self._get_file_handler = handler

    @property
    def fluctuation_handler(self):
        return self._fluctuation_handler

    @fluctuation_handler.setter
    def fluctuation_handler(self, handler):
        self._fluctuation_handler = handler

    @property
    def multipletest_handler(self):
        return self._multipletest_handler

    @multipletest_handler.setter
    def multipletest_handler(self, handler):
        self._multipletest_handler = handler
