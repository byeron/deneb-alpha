from scipy.stats import levene

from domain.feature_data import FeatureData
from domain.interface.fluctuation_config import IFluctuationConfig
from usecase.fluctuation import Fluctuation


class LeveneTest(Fluctuation):
    def __init__(self, config: IFluctuationConfig):
        super().__init__(config)

        if not hasattr(self.config, "control"):
            raise ValueError("control is required")
        if not hasattr(self.config, "experiment"):
            raise ValueError("experiment is required")
        if not hasattr(self.config, "alpha"):
            raise ValueError("alpha is required")

        self.control = self.config.control
        self.experiment = self.config.experiment
        self.alpha = self.config.alpha

    def run(self, feature_data: FeatureData):
        df = feature_data.matrix
        if self.control not in df.index:
            raise ValueError(f"control {self.control} not found in the index")
        if self.experiment not in df.index:
            raise ValueError(f"experiment {self.experiment} not found in the index")

        ctrl = df.loc[self.control, :]
        expr = df.loc[self.experiment, :]

        rejects = []
        p_values = []
        for ctrl_feature, expr_feature in zip(ctrl.columns, expr.columns):
            ctrl_data = ctrl[ctrl_feature]
            expr_data = expr[expr_feature]

            var_ctrl = ctrl_data.var()
            var_expr = expr_data.var()
            center = "mean"  # "median" でも可
            stat, p = levene(ctrl_data, expr_data, center=center)

            p_values.append(p)
            # 強制的に片側検定をするため、p値とrejectの状態が乖離する場合があることに注意
            if var_ctrl > var_expr:
                # 実験群の分散が小さい場合
                # p値に関わらずFalse
                rejects.append(False)
            else:
                rejects.append(p < self.alpha)

        return (p_values, rejects)

    def can_correction(self):
        return True
