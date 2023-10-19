import sys

import typer_cloup as typer

from container.post_file import PostFileContainer

app = typer.Typer()


@app.command()
def post(path: str) -> None:
    container = PostFileContainer()
    container.config.from_yaml("config.yml")  # URL/REPO_DIR
    container.config.from_dict(
        {
            "src_path": path,
        }
    )
    container.wire(modules=[sys.modules[__name__]])
    post_file_handler = container.post_file_handler()
    _id = post_file_handler.run(path)
    print(f"File ID: {_id}")


if __name__ == "__main__":
    app()