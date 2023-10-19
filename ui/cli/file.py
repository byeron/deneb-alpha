import sys

import typer_cloup as typer

from container.create_file import CreateFileContainer
from container.delete_file import DeleteFileContainer

app = typer.Typer()


@app.command()
def create(path: str) -> None:
    container = CreateFileContainer()
    container.config.from_yaml("config.yml")  # URL/REPO_DIR
    container.config.from_dict(
        {
            "src_path": path,
        }
    )
    container.wire(modules=[sys.modules[__name__]])
    create_file_handler = container.create_file_handler()
    _id = create_file_handler.run(path)
    print(f"File ID: {_id}")


@app.command()
def delete(file_id: str) -> None:
    container = DeleteFileContainer()
    container.config.from_yaml("config.yml")
    delete_file_handler = container.delete_file_handler()
    _id = delete_file_handler.run(file_id)
    print(f"File ID: {_id}")


if __name__ == "__main__":
    app()
