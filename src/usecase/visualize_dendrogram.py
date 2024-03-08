import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform


class VDendrogram:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        self.medium_dir = data["output_dir"]
        self.img_dir = data["img_dir"]
        self.img_path = None

    def plot(self, linkaged, features, cutoff, output_dir: str = "./output"):
        figsize = (12, 9)
        dpi = 300

        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax = fig.add_subplot(111)
        dendrogram(
            linkaged,
            ax=ax,
            labels=features,
            color_threshold=cutoff,
        )

        # Set plot param
        ax.set_title(f"cutoff: {cutoff}")
        ax.set_ylim(0, 1)

        plt.tight_layout()
        fig.savefig(f"{self.img_path}/dendrogram.png")
        fig.savefig(f"{self.img_path}/dendrogram.pdf")

    def run(self, _id: str, cutoff: float, method: str = "average") -> None:
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

        self.plot(linkaged, features, cutoff=cutoff)

        return
