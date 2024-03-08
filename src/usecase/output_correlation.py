import json

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
        self.json_path = f"{dst_dir}/{_id}/dissimilarity.json"
        self.metric = metric

    def output_humanreadable(self, correlation: pd.DataFrame):
        correlation.index = correlation.columns.tolist()
        correlation.to_csv(self.output_path, index=True)
        return None

    def output_json(self, correlation: pd.DataFrame):
        correlation.index = correlation.columns.tolist()
        d = {}
        d["metric"] = self.metric
        d["index"] = correlation.index.tolist()
        d["columns"] = correlation.columns.tolist()
        d["value"] = correlation.to_numpy().tolist()
        with open(self.json_path, "w") as f:
            json.dump(d, f, indent=2)
        return None

    def run(self, correlation: pd.DataFrame):
        correlation.index = correlation.columns.tolist()
        self.output_json(correlation)
        self.output_humanreadable(correlation)
        return correlation
