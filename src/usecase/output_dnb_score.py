import pandas as pd

from domain.interface.output_dnb_score import IOutputDNBScore


class OutputDNBScore(IOutputDNBScore):
    def __init__(
        self,
        _id: str,
        dst_dir: str = "./src/medium",
    ):
        self.output_path = f"{dst_dir}/{_id}/score.csv"

    def run(self, score: dict):
        a = pd.DataFrame.from_dict(score, orient="index")
        a.to_csv(self.output_path, index=True)
        return a
