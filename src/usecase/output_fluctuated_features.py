from domain.feature_data import FeatureData
from domain.interface.output_fluctuated_features import IOutputFluctuatedFeatures


class OutputFluctuatedFeatures(IOutputFluctuatedFeatures):
    def __init__(
        self,
        _id: str,
        dst_dir: str = "./src/medium",
    ):
        self.output_path = f"{dst_dir}/{_id}/fluctuated_features.csv"

    def run(self, data: FeatureData, reject: list):
        mask = [e for e, b in zip(data.features, reject) if b]
        df = data.matrix.loc[:, mask]
        df.to_csv(self.output_path)
