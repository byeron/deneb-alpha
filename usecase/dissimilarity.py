from domain.interface.dissimilarity import IDissimilarity
from domain.interface.dissimilarity_config import IDissimilarityConfig
from domain.interface.feature_data import IFeatureData


class Dissimilarity(IDissimilarity):
    def __init__(self, dissimilarity_config: IDissimilarityConfig):
        self.config = dissimilarity_config

    def run(self, feature_data: IFeatureData):
        pass
