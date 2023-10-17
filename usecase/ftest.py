from domain.interface.fluctuation_config import IFluctuationConfig
from usecase.fluctuation import Fluctuation


class Ftest(Fluctuation):
    def __init__(self, config: IFluctuationConfig):
        super().__init__(config)

        if not hasattr(self.config, "control"):
            raise AttributeError("control is not set")

        if not hasattr(self.config, "experiment"):
            raise AttributeError("experiment is not set")

        if not hasattr(self.config, "alpha"):
            raise AttributeError("alpha is not set")

        self.control = self.config.control
        self.experiment = self.config.experiment
        self.alpha = self.config.alpha

    def run(self):
        print("Ftest.run()")
        print(
            f"control: {self.control}, experiment: {self.experiment}, alpha: {self.alpha}"
        )
        return [[0.1, 0.2, 0.3], [True, False, True]]
