from typing import List, Optional

import typer_cloup as typer
from typing_extensions import Annotated

from usecase.visualize_dendrogram import VDendrogram
from usecase.visualize_dnb_score import VDNBScore

featuredata_input = {"id": None}


def callback(id: str):
    featuredata_input["id"] = id


app = typer.Typer(callback=callback)


@app.command()
def dendrogram(cutoff: float = 0.3, method: str = "average") -> None:
    # idの存在確認

    v = VDendrogram("./src/config.yml")
    v.run(featuredata_input["id"], cutoff, method)


@app.command()
def score(state: Optional[List[str]] = typer.Option(None)):
    print(f"state: {state}")
    v = VDNBScore("./src/config.yml")
    v.run(featuredata_input["id"], order=state)


if __name__ == "__main__":
    app()
