import sys

import typer_cloup as typer

from container.register_file import RegisterFileContainer
from container.delete_file import DeleteFileContainer
from container.read_files import ReadFilesContainer
from infrastructure.error import RepositoryError

app = typer.Typer()


@app.command()
def register(path: str) -> None:
    container = RegisterFileContainer()
    container.config.from_yaml("config.yml")  # URL/REPO_DIR
    container.config.from_dict(
        {
            "src_path": path,
        }
    )
    container.wire(modules=[sys.modules[__name__]])
    create_file_handler = container.handler()
    try:
        _id = create_file_handler.run(path)
    except RepositoryError as e:
        print(e)
        return
    print(f"File ID: {_id}")


@app.command()
def get() -> None:
    container = ReadFilesContainer()
    container.config.from_yaml("config.yml")
    read_files_handler = container.read_files_handler()
    try:
        feature_files = read_files_handler.run()
    except RepositoryError as e:
        print(e)
        return

    if not feature_files:
        print("No files registered.")
        return
    else:
        for feature_file in feature_files:
            print(f"ID: {feature_file.file_id}")
            print(f"\tName: {feature_file.file_name}")
            # print(f"Hash: {feature_file.hash}")
            print(f"\tCreated at: {feature_file.created_at}")


@app.command()
def delete(file_id: str) -> None:
    container = DeleteFileContainer()
    container.config.from_yaml("config.yml")
    delete_file_handler = container.delete_file_handler()
    try:
        _id = delete_file_handler.run(file_id)
    except RepositoryError as e:
        print(e)
        return
    print(f"File ID: {_id}")


if __name__ == "__main__":
    app()
