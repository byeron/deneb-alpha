from domain.interface.fluctuation_config import IFluctuationConfig
from usecase.fluctuation import Fluctuation
from domain.feature_data import FeatureData
from scipy.stats import f


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

        control = df.loc[self.control, :]
        experiment = df.loc[self.experiment, :]

        # Calculate F-value
        control_var = control.var(ddof=1, axis=0)
        experiment_var = experiment.var(ddof=1, axis=0)
        f_value = experiment_var / control_var
        p_value = f.sf(f_value, dfn=(len(experiment) - 1), dfd=(len(control) - 1))
        reject = [p_value < self.alpha for p_value in p_value]

        return (p_value, reject)