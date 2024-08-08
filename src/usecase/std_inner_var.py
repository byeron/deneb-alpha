from domain.feature_data import FeatureData
from domain.interface.fluctuation_config import IFluctuationConfig
from usecase.fluctuation import Fluctuation


class StdInnerVar(Fluctuation):
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

        # exprの各列ごとの標準偏差と平均値を計算
        std_expr = expr.std(axis=0)
        mean_expr = expr.mean(axis=0)

        # 実験群のstdが実験群のmeanの2倍以上の場合、True, それ以外はFalse
        diff = std_expr - mean_expr * self.threshold
        reject = diff > 0

        return (diff, reject)
