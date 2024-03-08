import typer_cloup as typer

from ui.cli import dnb_score, file, fluctuation, network, visualize

app = typer.Typer()
app.add_sub(fluctuation.app, name="fluctuation")
app.add_sub(file.app, name="file")
app.add_sub(network.app, name="network")
app.add_sub(dnb_score.app, name="dnb")
app.add_sub(visualize.app, name="visualize")

if __name__ == "__main__":
    app()
