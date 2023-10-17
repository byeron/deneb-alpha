import typer_cloup as typer

from ui.cli import fluctuation

app = typer.Typer()
app.add_sub(fluctuation.app, name="fluctuation")

if __name__ == "__main__":
    app()
