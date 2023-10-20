import sys

from container.fluctuation import FtestContainer, MultipletestContiner
from container.get_file import GetFileContainer


class WireFluctuation:
    def __init__(
        self,
        control: str,
        experiment: str,
        alpha: float,
        multipletest: bool,
        method: str,
    ):
        # Set default values
        self.get_file_handler = None
        self.fluctuation_handler = None
        self.multipletest_handler = None

        # Setup Handlers
        container = GetFileContainer()
        container.config.from_yaml("config.yml")
        container.wire(modules=[sys.modules[__name__]])
        self.get_file_handler = container.handler()

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
            return self.get_file_handler

        @property
        def fluctuation_handler(self):
            return self.fluctuation_handler

        @property
        def multipletest_handler(self):
            return self.multipletest_handler
