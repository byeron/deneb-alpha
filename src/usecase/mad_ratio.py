import numpy as np

from domain.feature_data import FeatureData
from domain.interface.fluctuation_config import IFluctuationConfig
from usecase.fluctuation import Fluctuation


class MadRatio(Fluctuation):
    def __init__(self, config: IFluctuationConfig):
        super().__init__(config)

        if not hasattr(self.config, "control"):
            raise AttributeError("control is required")
        if not hasattr(self.config, "experiment"):
            raise AttributeError("experiment is required")
        if not hasattr(self.config, "threshold"):
            raise AttributeError("mad_threshold is required")

        self.control = self.config.control
        self.experiment = self.config.experiment
        self.threshold = self.config.threshold

    def run(self, feature_data: FeatureData):
        df = feature_data.matrix

        if self.control not in df.index:
            raise ValueError(f"control {self.control} is not in the index")
        if self.experiment not in df.index:
            raise ValueError(f"experiment {self.experiment} is not in the index")

        ctrl = df.loc[self.control, :]
        expr = df.loc[self.experiment, :]

        # 各列ごとの中央絶対偏差を計算
        # controlのMAD
        mad_ctrl = np.median(np.abs(ctrl - ctrl.median(axis=0)), axis=0)
        mad_expr = np.median(np.abs(expr - expr.median(axis=0)), axis=0)

        # 実験群のMADが対象群のMADの2倍以上の場合、True, それ以外はFalse
        diff = mad_expr - mad_ctrl * self.threshold
        reject = diff > 0

        return (diff, reject)

    def can_correction(self):
        return False
