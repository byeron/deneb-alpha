import json
import os
from collections import OrderedDict

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from mpl_toolkits.axes_grid1 import ImageGrid


class VHeatmap:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        self.medium_dir = data["output_dir"]
        self.img_dir = data["img_dir"]
        self.img_path = None

    def plot(self, df, nn, order, vmin, vmax, label_span, output_dir: str = "./output"):
        corrs = OrderedDict()

        if order:
            if len(order) != len(df.index.unique()):
                raise ValueError("number of state is incorrect")
            for e in df.index.unique():
                if e not in order:
                    raise ValueError("state name is incorrect")
            for o in order:
                corrs[o] = df.loc[o, :].corr()
        else:
            for n, (t, d) in enumerate(df.groupby(level=0)):
                corrs[t] = d.corr()

        figsize = (9, 3)
        dpi = 300
        fig = plt.figure(figsize=figsize, dpi=dpi)
        grid = ImageGrid(
            fig,
            111,
            nrows_ncols=(1, len(df.index.unique())),
            cbar_location="bottom",
            cbar_mode="single",
            axes_pad=0.15,
            cbar_size="2.5%",
        )
        fig.canvas.draw()

        for (k, v), ax in zip(corrs.items(), grid):
            im = ax.imshow(
                v,
                vmin=vmin,
                vmax=vmax,
                cmap="RdBu_r",
                interpolation="none",
            )
            ax.set_xticks([n for n, i in enumerate(v.index) if n % label_span == 0])
            ax.set_xticklabels(
                [i for n, i in enumerate(v.index) if n % label_span == 0], rotation=0
            )
            ax.set_yticks([n for n, i in enumerate(v.index) if n % label_span == 0])
            ax.set_yticklabels(
                [i for n, i in enumerate(v.index) if n % label_span == 0]
            )
            ax.set_title(f"{k}")
        _ = grid.cbar_axes[0].colorbar(im)

        fig.savefig(f"{self.img_path}/heatmap_{nn+1}.png")
        fig.savefig(f"{self.img_path}/heatmap_{nn+1}.pdf")

    def run(
        self,
        _id: str,
        order: [],
        vmin: float,
        vmax: float,
        label_span: int,
    ) -> None:
        self.img_path = f"{self.img_dir}/{_id}"

        os.makedirs(self.img_path, exist_ok=True)

        # get medium file
        """
        df = pd.read_csv(
            # ここを変えて対応したい
            f"{self.medium_dir}/{_id}/fluctuated_features.csv",
            index_col=0,
            header=0,
        )
        """
        with open(f"{self.medium_dir}/{_id}/heatmap.json", "r") as f:
            d = json.load(f)

        for n, c in enumerate(d["clusters"]):
            df = pd.DataFrame(
                c["value"],
                index=c["index"],
                columns=c["columns"],
            )

            try:
                self.plot(df, n, order, vmin, vmax, label_span)
            except Exception as e:
                raise e

        return
