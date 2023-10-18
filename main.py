import typer_cloup as typer

from ui.cli import file, fluctuation

app = typer.Typer()
app.add_sub(fluctuation.app, name="fluctuation")
app.add_sub(file.app, name="file")

if __name__ == "__main__":
    app()
