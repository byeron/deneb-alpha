import pandas as pd

from domain.interface.output_fluctuation import IOutputFluctuation


class OutputFluctuationPval(IOutputFluctuation):
    def __init__(self, _id: str, method: str = "ftest", dst_dir: str = "./src/medium"):
        self.output_path = f"{dst_dir}/{_id}/{method}.csv"

    def run(
        self,
        features: list[str],
        pvals: list[float],
        reject: list[bool],
        pvals_corrected: list[float] = None,
    ) -> pd.DataFrame:
        # features, pvals, reject, pvals_correctedの順でDataFrameに変換
        # pvals_correctedがNoneの場合はpvals_correctedを追加しない
        # DataFrameをcsvに出力
        # pvals_correctedがNoneの場合はpvals_correctedを追加しない

        if pvals_corrected is None:
            df = pd.DataFrame(
                {
                    "features": features,
                    "p_values": pvals,
                    "reject": reject,
                }
            )
        else:
            df = pd.DataFrame(
                {
                    "features": features,
                    "p_values": pvals,
                    "p_values_corrected": pvals_corrected,
                    "reject": reject,
                }
            )

        # DataFrameをcsvに出力
        df.to_csv(self.output_path, index=False)

        return df
