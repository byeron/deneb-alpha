import json
import os
from collections import OrderedDict

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from mpl_toolkits.axes_grid1 import ImageGrid


def set_default(param, _default):
    if param is None:
        return _default
    else:
        return param


class VHeatmap:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        self.medium_dir = data["output_dir"]
        self.img_dir = data["img_dir"]
        self.img_path = None

    def plot(self, df, figparam, nth, order, output_dir: str = "./output"):
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
        xlabel = set_default(figparam["common"].xlabel, "Features")
        ylabel = set_default(figparam["common"].ylabel, "Features")
        vmin = set_default(figparam["heatmap"].vmin, -1)
        vmax = set_default(figparam["heatmap"].vmax, 1)
        labelfreq = set_default(figparam["heatmap"].labelfreq, 1)
        cmap = set_default(figparam["heatmap"].cmap, "RdBu_r")
        nrows = set_default(figparam["heatmap"].nrows, 1)
        ncols = set_default(figparam["heatmap"].ncols, len(df.index.unique()))
        cbar_loc = set_default(figparam["heatmap"].cbar_loc, "bottom")
        cbar_size = set_default(figparam["heatmap"].cbar_size, "2.5%")
        ax_pad = set_default(figparam["heatmap"].ax_pad, 0.2)

        # データの表示順を指定したものに並び替える
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

        if len(corrs.keys()) != (ncols * nrows):
            print(
                f"Warning: length({len(corrs.keys())}) does not correspond to nrows ({nrows}) * ncols ({ncols})"
            )

        figsize = (sizex, sizey)
        dpi = 300

        fig = plt.figure(figsize=figsize, dpi=dpi)
        fig.suptitle(title)
        grid = ImageGrid(
            fig,
            111,
            nrows_ncols=(nrows, ncols),
            cbar_location=cbar_loc,
            cbar_mode="single",
            axes_pad=ax_pad,
            cbar_size=cbar_size,
        )
        fig.canvas.draw()

        for nn, ((k, v), ax) in enumerate(zip(corrs.items(), grid)):
            print(k)
            im = ax.imshow(
                v,
                vmin=vmin,
                vmax=vmax,
                cmap=cmap,
                interpolation="none",
            )

            if nn == 0:
                ax.set_ylabel(ylabel, fontsize=ylabelsize)

            if nn == (len(corrs.keys()) - ncols):
                ax.set_xlabel(xlabel, fontsize=xlabelsize)

            ax.set_xticks([n for n, i in enumerate(v.index) if n % labelfreq == 0])
            ax.set_xticklabels(
                [i for n, i in enumerate(v.index) if n % labelfreq == 0],
            )
            ax.tick_params(
                which="both",
                axis="x",
                labelrotation=rotx,
                labelsize=xticklabelsize,
            )

            ax.set_yticks([n for n, i in enumerate(v.index) if n % labelfreq == 0])
            ax.set_yticklabels([i for n, i in enumerate(v.index) if n % labelfreq == 0])
            ax.tick_params(
                which="both",
                axis="y",
                labelrotation=roty,
                labelsize=yticklabelsize,
            )

            ax.set_title(f"{k}", fontsize=titlesize)
            ax.tick_params(which="both", axis="both", direction="in")

        _ = grid.cbar_axes[0].colorbar(im)
        grid.cbar_axes[0].tick_params(
            which="both",
            axis="both",
            direction="out",
        )

        fig.savefig(f"{self.img_path}/heatmap_{nth+1}.png", bbox_inches="tight")
        fig.savefig(f"{self.img_path}/heatmap_{nth+1}.pdf", bbox_inches="tight")

    def run(
        self,
        _id: str,
        figparam: dict,
        order: [],
    ) -> None:
        self.img_path = f"{self.img_dir}/{_id}"

        os.makedirs(self.img_path, exist_ok=True)

        with open(f"{self.medium_dir}/{_id}/heatmap.json", "r") as f:
            d = json.load(f)

        for nth, c in enumerate(d["clusters"], start=1):
            df = pd.DataFrame(
                c["value"],
                index=c["index"],
                columns=c["columns"],
            )

            try:
                self.plot(df, figparam, nth, order)
            except Exception as e:
                raise e

        return
