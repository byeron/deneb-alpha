from dataclasses import dataclass
from typing import List, Optional

import typer
from typing_extensions import Annotated

from usecase.visualize_dendrogram import VDendrogram
from usecase.visualize_dnb_score import VDNBScore
from usecase.visualize_heatmap import VHeatmap

featuredata_input = {"id": None}


@dataclass
class CommonFigParam:
    sizex: float
    sizey: float
    rotx: float
    roty: float
    title: str = None
    xlabel: str = None
    ylabel: str = None
    xticklabelsize: float = None
    yticklabelsize: float = None
    xlabelsize: float = None
    ylabelsize: float = None


@dataclass
class DendrogramFigParam:
    ymax: float = 1.0
    ymin: float = 0.0


@dataclass
class ScoreFigParam:
    xmin: float = None
    ymin: float = None
    xgridmajfreq: int = None
    xgridminfreq: int = None
    score_max: float = 1.0
    score_min: float = 0.0
    std_max: float = 1.0
    std_min: float = 0.0
    corr_max: float = 1.0
    corr_min: float = 0.0


@dataclass
class HeatmapFigParam:
    vmin: float = None
    vmax: float = None
    labelfreq: int = None
    nrows: int = None
    ncols: int = None
    cmap: str = None
    cbar_loc: str = None
    cbar_size: float = None
    ax_pad: float = None


def callback(
    ctx: typer.Context,
    id: Annotated[str, typer.Argument()],
    sizex: Annotated[Optional[float], typer.Option(help="figsize of x-axis")] = None,
    sizey: Annotated[Optional[float], typer.Option(help="figsize of y-axis")] = None,
    rotx: Annotated[
        Optional[float], typer.Option(help="rotation of xticklabels")
    ] = None,
    roty: Annotated[
        Optional[float], typer.Option(help="rotation of yticklabels")
    ] = None,
    title: Annotated[Optional[str], typer.Option(help="figure title")] = None,
    xlabel: Annotated[Optional[str], typer.Option(help="x-axis label")] = None,
    ylabel: Annotated[Optional[str], typer.Option(help="y-axis label")] = None,
    xticklabelsize: Annotated[
        Optional[float], typer.Option(help="x-axis ticklabel size")
    ] = None,
    yticklabelsize: Annotated[
        Optional[float], typer.Option(help="y-axis ticklabel size")
    ] = None,
    xlabelsize: Annotated[
        Optional[float], typer.Option(help="x-axis label size")
    ] = None,
    ylabelsize: Annotated[
        Optional[float], typer.Option(help="y-axis label size")
    ] = None,
    ymax: Annotated[
        Optional[float], typer.Option(help="y-axis max range [dendrogram]")
    ] = 1.0,
    ymin: Annotated[
        Optional[float], typer.Option(help="y-axis min range [dendrogram]")
    ] = 0.0,
    score_max: Annotated[
        Optional[float], typer.Option(help="DNBscore-axis max range [DNB score]")
    ] = None,
    score_min: Annotated[
        Optional[float], typer.Option(help="DNBscore-axis min range [DNB score]")
    ] = None,
    std_max: Annotated[
        Optional[float], typer.Option(help="STD deviation-axis max range [DNB score]")
    ] = None,
    std_min: Annotated[
        Optional[float], typer.Option(help="STD deviation-axis min range [DNB score]")
    ] = None,
    corr_max: Annotated[
        Optional[float], typer.Option(help="Correlaton-axis max range [DNB score]")
    ] = 1.0,
    corr_min: Annotated[
        Optional[float], typer.Option(help="Correlation-axis min range [DNB score]")
    ] = 0.0,
    xgridmajfreq: Annotated[
        Optional[int], typer.Option(help="Major grid frequency [DNB score]")
    ] = None,
    xgridminfreq: Annotated[
        Optional[int], typer.Option(help="Minor grid frequency [DNB score]")
    ] = None,
    vmin: Annotated[Optional[float], typer.Option(help="vmin [Heatmap]")] = None,
    vmax: Annotated[Optional[float], typer.Option(help="vmax [Heatmap]")] = None,
    labelfreq: Annotated[
        Optional[int], typer.Option(help="label frequency [Heatmap]")
    ] = 5,
    nrows: Annotated[
        Optional[int], typer.Option(help="number of rows [Heatmap]")
    ] = None,
    ncols: Annotated[
        Optional[int], typer.Option(help="number of cols [Heatmap]")
    ] = None,
    cmap: Annotated[Optional[str], typer.Option(help="color map [Heatmap]")] = "RdBu_r",
    cbar_loc: Annotated[
        Optional[str], typer.Option(help="color bar location [Heatmap]")
    ] = "bottom",
    cbar_size: Annotated[
        Optional[float], typer.Option(help="color bar size [Heatmap]")
    ] = 2.5,
    ax_pad: Annotated[
        Optional[float], typer.Option(help="padding between each axes [Heatmap]")
    ] = 0.15,
):
    featuredata_input["id"] = id

    cfp = CommonFigParam(
        sizex=sizex,
        sizey=sizey,
        rotx=rotx,
        roty=roty,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        xticklabelsize=xticklabelsize,
        yticklabelsize=yticklabelsize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
    )
    dfp = DendrogramFigParam(
        ymax=ymax,
        ymin=ymin,
    )
    sfp = ScoreFigParam(
        score_max=score_max,
        score_min=score_min,
        std_max=std_max,
        std_min=std_min,
        corr_max=corr_max,
        corr_min=corr_min,
        xgridmajfreq=xgridmajfreq,
        xgridminfreq=xgridminfreq,
    )
    hfp = HeatmapFigParam(
        vmax=vmax,
        vmin=vmin,
        labelfreq=labelfreq,
        nrows=nrows,
        ncols=ncols,
        cmap=cmap,
        cbar_loc=cbar_loc,
        cbar_size=f"{cbar_size}%",
        ax_pad=ax_pad,
    )
    print(dfp)
    ctx.obj = {"common": cfp, "dendrogram": dfp, "score": sfp, "heatmap": hfp}


app = typer.Typer(callback=callback)


@app.command()
def dendrogram(
    ctx: typer.Context,
    cutoff: Annotated[float, typer.Option()] = 0.5,
    method: Annotated[str, typer.Option()] = "average",
) -> None:
    # idの存在確認
    v = VDendrogram("./src/config.yml")
    v.run(featuredata_input["id"], ctx.obj, cutoff, method)


@app.command()
def score(
    ctx: typer.Context,
    order: Annotated[
        Optional[list[str]], typer.Option("--order", "-o", help="order state")
    ] = None,
    ignore_state: Annotated[
        Optional[list[str]], typer.Option("--ignore-state", "-ign", help="ignore state")
    ] = None,
    unit: Annotated[
        Optional[str], typer.Option("--unit", "-u", help="ignore state")
    ] = None,
):
    print(f"order: {order}")
    print(f"ignore state: {ignore_state}")
    v = VDNBScore("./src/config.yml")
    v.run(
        featuredata_input["id"],
        ctx.obj,
        order=order,
        ignore_state=ignore_state,
        unit=unit,
    )


@app.command()
def heatmap(
    ctx: typer.Context,
    order: Annotated[
        Optional[list[str]], typer.Option("--order", "-o", help="order state")
    ] = None,
):
    v = VHeatmap("./src/config.yml")
    try:
        v.run(featuredata_input["id"], ctx.obj, order)
    except Exception as e:
        print(e)
        return


if __name__ == "__main__":
    app()
