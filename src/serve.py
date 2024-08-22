import typer
from ui.cli import dnb_score, file, fluctuation, network, visualize

app = typer.Typer()
app.add_typer(fluctuation.app, name="fluctuation")
app.add_typer(file.app, name="file")
app.add_typer(network.app, name="network")
app.add_typer(dnb_score.app, name="dnb")
app.add_typer(visualize.app, name="visualize")

if __name__ == "__main__":
    app()
