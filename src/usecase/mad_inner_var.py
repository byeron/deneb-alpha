import numpy as np

from domain.feature_data import FeatureData
from domain.interface.fluctuation_config import IFluctuationConfig
from usecase.fluctuation import Fluctuation


class MadInnerVar(Fluctuation):
    def __init__(self, config: IFluctuationConfig):
        super().__init__(config)

        if not hasattr(self.config, "experiment"):
            raise AttributeError("experiment is required")
        if not hasattr(self.config, "threshold"):
            raise AttributeError("mad_threshold is required")

        self.experiment = self.config.experiment
        self.threshold = self.config.threshold

    def run(self, feature_data: FeatureData):
        df = feature_data.matrix

        if self.experiment not in df.index:
            raise ValueError(f"experiment {self.experiment} is not in the index")

        expr = df.loc[self.experiment, :]

        # 各列ごとの中央絶対偏差を計算
        # exprのMAD
        mad_expr = np.median(np.abs(expr - expr.median(axis=0)), axis=0)
        # exprの中央値
        median_expr = expr.median(axis=0)

        # 実験群のMADが実験群のmeanの2倍以上の場合、True, それ以外はFalse
        diff = mad_expr - median_expr * self.threshold
        reject = diff > 0

        return (diff, reject)
