import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform


def set_default(param, _default):
    if param is None:
        return _default
    else:
        return param


class VDendrogram:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        self.medium_dir = data["output_dir"]
        self.img_dir = data["img_dir"]
        self.img_path = None

    def plot(self, figparam, linkaged, features, cutoff, output_dir: str = "./output"):
        sizex = set_default(figparam["common"].sizex, 9)
        sizey = set_default(figparam["common"].sizey, 9)
        rotx = set_default(figparam["common"].rotx, 0)
        title = set_default(figparam["common"].title, f"cutoff: {cutoff}")
        titlesize = set_default(figparam["common"].titlesize, None)
        xticklabelsize = set_default(figparam["common"].xticklabelsize, None)
        yticklabelsize = set_default(figparam["common"].yticklabelsize, None)
        xlabelsize = set_default(figparam["common"].xlabelsize, None)
        ylabelsize = set_default(figparam["common"].ylabelsize, None)
        xlabel = set_default(figparam["common"].xlabel, "Features")
        ylabel = set_default(figparam["common"].ylabel, "Dissimilarity")
        ymin = set_default(figparam["dendrogram"].ymin, 0)
        ymax = set_default(figparam["dendrogram"].ymax, 1)

        figsize = (sizex, sizey)
        dpi = 300

        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax = fig.add_subplot(111)
        dendrogram(
            linkaged,
            ax=ax,
            labels=features,
            color_threshold=cutoff,
            leaf_rotation=rotx,
            leaf_font_size=xticklabelsize,
        )

        # Set plot param
        ax.set_title(title, fontsize=titlesize)
        ax.set_xlabel(xlabel, fontsize=xlabelsize)
        ax.set_ylabel(ylabel, fontsize=ylabelsize)
        ax.tick_params(axis="y", labelsize=yticklabelsize)
        ax.set_ylim(ymin, ymax)

        plt.tight_layout()
        fig.savefig(f"{self.img_path}/dendrogram.png")
        fig.savefig(f"{self.img_path}/dendrogram.pdf")

    def run(
        self, _id: str, figparam: dict, cutoff: float, method: str = "average"
    ) -> None:
        self.img_path = f"{self.img_dir}/{_id}"

        os.makedirs(self.img_path, exist_ok=True)

        # get medium file
        with open(f"{self.medium_dir}/{_id}/dissimilarity.json") as f:
            d = json.load(f)
        df = pd.DataFrame(d["value"], index=d["index"], columns=d["columns"])
        print(df)

        # create images
        features = df.columns
        dissimilarity = df.to_numpy()

        dissimilarity = squareform(dissimilarity)
        linkaged = linkage(dissimilarity, method=method)

        self.plot(figparam, linkaged, features, cutoff=cutoff)

        return
