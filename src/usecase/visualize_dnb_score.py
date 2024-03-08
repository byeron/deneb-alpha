import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import yaml


class VDNBScore:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        self.medium_dir = data["output_dir"]
        self.img_dir = data["img_dir"]
        self.img_path = None

    def common(self, data, nn):
        figsize = (9, 3)
        dpi = 300

        fig = plt.figure(figsize=figsize, dpi=dpi)

        d = data.loc["dnb_score", :]
        ax = fig.add_subplot(1, 3, 1)
        ax.plot(d.to_numpy(), color="tab:red", marker="o")
        ax.set_ylabel("DNB Score")
        ax.set_xticks([n for n, _ in enumerate(d.index)])
        ax.set_xticklabels(list(d.index))
        ax.set_xlabel("state")
        ax.grid(which="both", axis="both")

        d = data.loc["std_deviation", :]
        ax = fig.add_subplot(1, 3, 2)
        ax.plot(d.to_numpy(), color="tab:blue", marker="o")
        ax.set_ylabel("Average Std")
        ax.set_xticks([n for n, _ in enumerate(d.index)])
        ax.set_xticklabels(list(d.index))
        ax.set_xlabel("state")
        ax.grid(which="both", axis="both")

        d = data.loc["corr_strength", :]
        ax = fig.add_subplot(1, 3, 3)
        ax.plot(d.to_numpy(), color="tab:purple", marker="o")
        ax.set_ylabel("Average Corr")
        ax.set_xticks([n for n, _ in enumerate(d.index)])
        ax.set_xticklabels(list(d.index))
        ax.set_xlabel("state")
        # ax.set_ylim(-1, 1)
        ax.grid(which="both", axis="both")

        plt.tight_layout()
        fig.savefig(f"{self.img_path}/score_{nn}.png")
        fig.savefig(f"{self.img_path}/score_{nn}.pdf")

    def with_order(self, score, order, output_dir):
        if len(list(score[0]["dnb_score"].keys())) != len(order):
            raise ValueError("number of states is incorrect")

        for e in list(score[0]["dnb_score"].keys()):
            if e not in order:
                raise ValueError("state name is incorrect")

        for nn, s in enumerate(score):
            _ = s.pop("features")
            data = pd.DataFrame.from_dict(s, orient="index")
            data = data.reindex(columns=order)

            self.common(data, nn)

    def without_order(self, score, output_dir):
        for nn, s in enumerate(score):
            _ = s.pop("features")
            data = pd.DataFrame.from_dict(s, orient="index")
            self.common(data, nn)

    def plot(self, score: list, order: list, output_dir: str = "./output"):
        if order:
            try:
                self.with_order(score, order, output_dir)
            except Exception as e:
                print(e)
                return

        else:
            self.without_order(score, output_dir)

        return

    def run(self, _id: str, order: list = []) -> None:
        self.img_path = f"{self.img_dir}/{_id}"

        os.makedirs(self.img_path, exist_ok=True)

        # get medium file
        with open(f"{self.medium_dir}/{_id}/score.json") as f:
            d = json.load(f)
        self.plot(d, order)

        print(self.img_path)

        return
