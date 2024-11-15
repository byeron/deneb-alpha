import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from matplotlib.ticker import MultipleLocator


def set_default(param, _default):
    if param is None:
        return _default
    else:
        return param


class VDNBScore:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        self.medium_dir = data["output_dir"]
        self.img_dir = data["img_dir"]
        self.img_path = None

    def plot(self, data, figparam, nth):
        sizex = set_default(figparam["common"].sizex, 12)
        sizey = set_default(figparam["common"].sizey, 4)
        rotx = set_default(figparam["common"].rotx, 0)
        roty = set_default(figparam["common"].roty, 0)
        xticklabelsize = set_default(figparam["common"].xticklabelsize, None)
        yticklabelsize = set_default(figparam["common"].yticklabelsize, None)
        title = set_default(figparam["common"].title, None)
        titlesize = set_default(figparam["common"].titlesize, None)
        xlabelsize = set_default(figparam["common"].xlabelsize, None)
        ylabelsize = set_default(figparam["common"].ylabelsize, None)
        xlabel = set_default(figparam["common"].xlabel, "States")
        score_min = set_default(figparam["score"].score_min, None)
        score_max = set_default(figparam["score"].score_max, None)
        std_min = set_default(figparam["score"].std_min, None)
        std_max = set_default(figparam["score"].std_max, None)
        corr_min = set_default(figparam["score"].corr_min, None)
        corr_max = set_default(figparam["score"].corr_max, None)
        xgridmajfreq = set_default(figparam["score"].xgridmajfreq, None)
        xgridminfreq = set_default(figparam["score"].xgridminfreq, None)

        figsize = (sizex, sizey)
        dpi = 300

        fig = plt.figure(figsize=figsize, dpi=dpi)

        # Plot DNB score
        d = data.loc["dnb_score", :]
        ax = fig.add_subplot(1, 3, 1)
        ax.plot(d.index, d, color="tab:red", marker="o")

        ax.set_xlabel(xlabel, fontsize=xlabelsize)
        ax.set_ylabel("$I_{\mathrm{DNB}}$", fontsize=ylabelsize)
        ax.tick_params(axis="x", labelsize=xticklabelsize, labelrotation=rotx)
        ax.tick_params(axis="y", labelsize=yticklabelsize, labelrotation=roty)
        ax.tick_params(axis="both", which="both", direction="in")
        ax.set_ylim(score_min, score_max)
        ax.grid(which="both", axis="both")
        if xgridmajfreq is not None:
            ax.xaxis.set_major_locator(MultipleLocator(xgridmajfreq))
            if xgridminfreq is not None:
                ax.xaxis.set_minor_locator(MultipleLocator(xgridminfreq))

        # Plot Mean Standard Deviation
        d = data.loc["std_deviation", :]
        ax = fig.add_subplot(1, 3, 2)
        ax.plot(d.index, d, color="tab:blue", marker="o")

        ax.set_title(title, fontsize=titlesize)
        ax.set_xlabel(xlabel, fontsize=xlabelsize)
        ax.set_ylabel("$I_{\mathrm{s}}$", fontsize=ylabelsize)
        ax.tick_params(axis="x", labelsize=xticklabelsize, labelrotation=rotx)
        ax.tick_params(axis="y", labelsize=yticklabelsize, labelrotation=roty)
        ax.tick_params(axis="both", which="both", direction="in")
        ax.set_ylim(std_min, std_max)
        ax.grid(which="both", axis="both")
        if xgridmajfreq is not None:
            ax.xaxis.set_major_locator(MultipleLocator(xgridmajfreq))
            if xgridminfreq is not None:
                ax.xaxis.set_minor_locator(MultipleLocator(xgridminfreq))

        # Plot Mean Correlation Strength
        d = data.loc["corr_strength", :]
        ax = fig.add_subplot(1, 3, 3)
        ax.plot(d.index, d, color="tab:purple", marker="o")

        ax.set_xlabel(xlabel, fontsize=xlabelsize)
        ax.set_ylabel("$I_{\mathrm{r}}$", fontsize=ylabelsize)
        ax.tick_params(axis="x", labelsize=xticklabelsize, labelrotation=rotx)
        ax.tick_params(axis="y", labelsize=yticklabelsize, labelrotation=roty)
        ax.tick_params(axis="both", which="both", direction="in")
        ax.set_ylim(corr_min, corr_max)
        ax.grid(which="both", axis="both")
        if xgridmajfreq is not None:
            ax.xaxis.set_major_locator(MultipleLocator(xgridmajfreq))
            if xgridminfreq is not None:
                ax.xaxis.set_minor_locator(MultipleLocator(xgridminfreq))

        # Output per clusters
        plt.tight_layout()
        fig.savefig(f"{self.img_path}/score_{nth}.png")
        fig.savefig(f"{self.img_path}/score_{nth}.pdf")

    def preprocess(
        self,
        scores: list,
        order: list,
        ignore_state: list,
        unit: str,
        output_dir: str = "./output",
    ):
        data = []
        for nth, score in enumerate(scores):
            _ = score.pop("features")
            d = pd.DataFrame.from_dict(score, orient="index")

            if ignore_state:  # もしオプションにより無視する状態があれば取り除く
                for _is in ignore_state:
                    if _is not in d.columns:
                        raise ValueError("ignore state name is incorrect")
                d = d.drop(columns=ignore_state)

            if order:  # もしオプションによる順序の指定があれば並び替える
                if len(d.columns) != len(order):
                    raise ValueError("number of states is incorrect")
                for o in order:
                    if o not in d.columns:
                        raise ValueError("state name is incorrect")

                d = d.reindex(columns=order)

            if unit is not None:
                # unitの文字列をcolumnsから取り除き、整数型にする
                # 時系列データの場合は不等間隔のデータがきれいに描画できる
                d.columns = [int(c.replace(unit, "")) for c in d.columns]

            print(d)
            data.append(d)
        return data

    def run(
        self,
        _id: str,
        figparam: dict,
        order: list = [],
        ignore_state: list = [],
        unit: str = None,
    ) -> None:
        self.img_path = f"{self.img_dir}/{_id}"

        os.makedirs(self.img_path, exist_ok=True)

        # get medium file
        with open(f"{self.medium_dir}/{_id}/score.json") as f:
            d = json.load(f)
        data = self.preprocess(d, order, ignore_state, unit)

        for nth, d in enumerate(data, start=1):
            self.plot(d, figparam, nth)

        print(self.img_path)
        return
