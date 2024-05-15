import json

from domain.feature_data import FeatureData
from domain.interface.output_heatmap import IOutputHeatmap


class OutputHeatmap(IOutputHeatmap):
    def __init__(
        self,
        _id: str,
        dst_dir: str = "./src/medium",
    ):
        self.output_path = f"{dst_dir}/{_id}/heatmap.json"

    def run(
        self,
        data: FeatureData,
        clusters: list[list[str]],
    ):
        result = []
        for i, elements in enumerate(clusters):
            a = {}
            d = data.matrix.loc[:, elements]
            a["index"] = d.index.to_list()
            a["columns"] = d.columns.to_list()
            a["value"] = d.to_numpy().tolist()
            result.append(a)

        r = {"clusters": result}
        with open(self.output_path, "w") as f:
            json.dump(r, f)
