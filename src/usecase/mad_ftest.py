import numpy as np
from scipy.stats import f

from domain.feature_data import FeatureData
from domain.interface.fluctuation_config import IFluctuationConfig
from usecase.fluctuation import Fluctuation


class MadFtest(Fluctuation):
    def __init__(self, config: IFluctuationConfig):
        super().__init__(config)

        if not hasattr(self.config, "control"):
            raise ValueError("config.control is required")
        if not hasattr(self.config, "experiment"):
            raise ValueError("config.experiment is required")
        if not hasattr(self.config, "alpha"):
            raise ValueError("config.alpha is required")

        self.control = self.config.control
        self.experiment = self.config.experiment
        self.alpha = self.config.alpha

    def run(self, feature_data: FeatureData):
        df = feature_data.matrix
        if self.control not in df.index:
            raise ValueError(f"control '{self.control}' is not in the index")
        if self.experiment not in df.index:
            raise ValueError(f"experiment '{self.experiment}' is not in the index")

        ctrl = df.loc[self.control, :]
        expr = df.loc[self.experiment, :]

        mad_ctrl = np.median(np.abs(ctrl - np.median(ctrl, axis=0)), axis=0)
        mad_expr = np.median(np.abs(expr - np.median(expr, axis=0)), axis=0)

        # 正規分布を仮定した場合、MAD*1.4826が標準偏差に相当する
        # が、分母分子に同じスケールを掛けるので、キャンセルされる
        # mad_ctrl *= 1.4826
        # mad_expr *= 1.4826

        # 分散と同じスケールへ変更
        var_ctrl = mad_ctrl**2
        var_expr = mad_expr**2

        f_value = var_expr / var_ctrl
        p_value = f.sf(f_value, len(expr) - 1, len(ctrl) - 1)
        reject = [p_value < self.alpha for p_value in p_value]

        return (p_value, reject)

    def can_correction(self):
        return True
