import pandas as pd

from domain.interface.output_fluctuation import IOutputFluctuation


class OutputFluctuationDiff(IOutputFluctuation):
    def __init__(self, _id: str, method: str = "ftest", dst_dir: str = "./src/medium"):
        self.output_path = f"{dst_dir}/{_id}/{method}.csv"

    def run(
        self,
        features: list[str],
        evals: list[float],
        reject: list[bool],
    ) -> pd.DataFrame:
        df = pd.DataFrame(
            {
                "features": features,
                "evaluates": evals,
                "reject": reject,
            }
        )

        # DataFrameをcsvに出力
        df.to_csv(self.output_path, index=False)

        return df
