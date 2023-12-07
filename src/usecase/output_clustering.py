import pandas as pd

from domain.interface.output_clustering import IOutputClustering


class OutputClustering(IOutputClustering):
    def __init__(
        self,
        _id: str,
        cutoff: float = 0.05,
        rank: int = 1,
        dst_dir: str = "./src/medium",
    ):
        cutoff = str(cutoff).replace(".", "_")
        self.output_path = f"{dst_dir}/{_id}/cluster-{cutoff}-{rank}.csv"

    def run(self, clusters: list[list[str]]):
        df = pd.DataFrame()
        for i, elements in enumerate(clusters):
            # 列方向に追加する
            df[i] = elements
        # CSVに変換する
        df.to_csv(self.output_path)
