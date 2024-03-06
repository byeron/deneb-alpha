import typer_cloup as typer

from ui.cli import file, fluctuation, network, dnb_score

app = typer.Typer()
app.add_sub(fluctuation.app, name="fluctuation")
app.add_sub(file.app, name="file")
app.add_sub(network.app, name="network")
app.add_sub(dnb_score.app, name="dnb")

if __name__ == "__main__":
    app()
