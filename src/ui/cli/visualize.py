from typing import List, Optional

import typer_cloup as typer

from usecase.visualize_dendrogram import VDendrogram
from usecase.visualize_dnb_score import VDNBScore
from usecase.visualize_heatmap import VHeatmap

featuredata_input = {"id": None}


def callback(id: str):
    featuredata_input["id"] = id


app = typer.Typer(callback=callback)


@app.command()
def dendrogram(cutoff: float = 0.5, method: str = "average") -> None:
    # idの存在確認

    v = VDendrogram("./src/config.yml")
    v.run(featuredata_input["id"], cutoff, method)


@app.command()
def score(state: Optional[List[str]] = typer.Option(None)):
    print(f"state: {state}")
    v = VDNBScore("./src/config.yml")
    v.run(featuredata_input["id"], order=state)


@app.command()
def heatmap(
    state: Optional[List[str]] = typer.Option(None),
    vmin: float = -1.0,
    vmax: float = 1.0,
    label_span: int = 5,
):
    v = VHeatmap("./src/config.yml")
    try:
        v.run(featuredata_input["id"], state, vmin, vmax, label_span)
    except Exception as e:
        print(e)
        return


if __name__ == "__main__":
    app()
