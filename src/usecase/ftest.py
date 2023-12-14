from scipy.stats import f

from domain.feature_data import FeatureData
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

    def run(self, feature_data: FeatureData):
        df = feature_data.matrix
        # Check if the control and experiment index exist
        if self.control not in df.index:
            raise ValueError(f"{self.control} is not in the index")
        if self.experiment not in df.index:
            raise ValueError(f"{self.experiment} is not in the index")

        control = df.loc[self.control, :]
        experiment = df.loc[self.experiment, :]

        # Calculate F-value
        control_var = control.var(ddof=1, axis=0)
        experiment_var = experiment.var(ddof=1, axis=0)

        # Control群の各カラムに分散が0のものが含まれている場合、0除算によるエラーをthrowする
        if control_var.isin([0]).any():
            # 分散が0の要素名を取得
            zero_var_columns = control_var[control_var == 0].index.tolist()
            raise ValueError(f"Control group has zero variance columns: {zero_var_columns}")

        f_value = experiment_var / control_var
        p_value = f.sf(f_value, dfn=(len(experiment) - 1), dfd=(len(control) - 1))
        reject = [p_value < self.alpha for p_value in p_value]

        return (p_value, reject)
