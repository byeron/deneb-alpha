from domain.interface.fluctuation import IFluctuation
from domain.interface.fluctuation_config import IFluctuationConfig


class Fluctuation(IFluctuation):
    def __init__(self, config: IFluctuationConfig):
        self.config = config

    def run(self):
        pass
