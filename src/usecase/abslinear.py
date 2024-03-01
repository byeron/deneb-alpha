from usecase.dissimilarity import Dissimilarity
from domain.interface.dissimilarity_config import IDissimilarityConfig
from injector import inject


class AbsLinear(Dissimilarity):
    @inject
    def __init__(self, dissimilarity_config: IDissimilarityConfig):
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
