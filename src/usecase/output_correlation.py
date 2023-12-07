import pandas as pd

from domain.interface.output_correlation import IOutputCorrelation


class OutputCorrelation(IOutputCorrelation):
    def __init__(
        self,
        _id: str,
        metric: str = "abslinear",
        dst_dir: str = "./src/medium",
    ):
        self.output_path = f"{dst_dir}/{_id}/{metric}.csv"

    def run(self, correlation: pd.DataFrame):
        correlation.index = correlation.columns.tolist()
        correlation.to_csv(self.output_path, index=True)
        return correlation
