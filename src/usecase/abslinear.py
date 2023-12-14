from usecase.dissimilarity import Dissimilarity


class AbsLinear(Dissimilarity):
    def __init__(self, dissimilarity_config):
        super().__init__(dissimilarity_config)

    def run(self, feature_data):
        f = feature_data.fluctuation
        if f.empty:
            raise ValueError("The fluctuating variable does not exist.")

        # 指定したexperimentがindexに存在しない場合、エラーを返す
        if self.config.experiment not in f.index:
            raise ValueError(
                f"The experiment '{self.config.experiment}' does not exist."
            )

        f = f.loc[self.config.experiment, :]

        dissimilarity = 1 - abs(f.corr(method=self.config.corr_method))
        dissimilarity[dissimilarity < 0] = 0
        return dissimilarity
