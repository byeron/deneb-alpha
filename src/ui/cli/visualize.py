import typer_cloup as typer

from usecase.visualize_dendrogram import VDendrogram

featuredata_input = {"id": None}


def callback(id: str):
    featuredata_input["id"] = id


app = typer.Typer(callback=callback)


@app.command()
def dendrogram(cutoff: float = 0.3, method: str = "average") -> None:
    # idの存在確認

    v = VDendrogram("./src/config.yml")
    v.run(featuredata_input["id"], cutoff, method)


if __name__ == "__main__":
    app()
