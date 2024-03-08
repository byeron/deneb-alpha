import pandas as pd
import json

from domain.interface.output_dnb_score import IOutputDNBScore


class OutputDNBScore(IOutputDNBScore):
    def __init__(
        self,
        _id: str,
        dst_dir: str = "./src/medium",
    ):
        self.output_dir = f"{dst_dir}/{_id}"
        self.json_path = f"{dst_dir}/{_id}/score.json"

    def human_readable(self, score):
        result = []
        for n, e in enumerate(score):
            std_dev = e["std_deviation"]
            corr_str = e["corr_strength"]
            dnb_score = e["dnb_score"]
            # features = e["featrures"]

            df = pd.DataFrame(columns=list(std_dev.keys()), index=["dnb_score", "std_deviation", "corr_strength"])
            for k, v in std_dev.items():
                df.loc["std_deviation", k]=v
                df.loc["corr_strength", k]=corr_str[k]
                df.loc["dnb_score", k]=dnb_score[k]
            df.to_csv(f"{self.output_dir}/score_{n}.csv", index=True)
            result.append(df)

        return result

    def output_json(self, score):
        with open(self.json_path, "w") as f:
            json.dump(score, f, indent=2)

    def run(self, score: list):
        a = self.human_readable(score)
        self.output_json(score)
        return a
