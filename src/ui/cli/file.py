import typer_cloup as typer

from injector import Injector

from domain.interface.register_file import IRegisterFile
from domain.interface.get_files import IGetFiles
from domain.interface.delete_file import IDeleteFile
from factory.delete_file import DeleteFileFactory
from factory.get_files import GetFilesFactory
from factory.register_file import RegisterFileFactory



app = typer.Typer()


@app.command()
def register(path: str) -> None:
    factory = RegisterFileFactory(
        "./src/config.yml"
    )
    injector = Injector(factory.configure)
    register_file_handler = injector.get(IRegisterFile)
    try:
        _id = register_file_handler.run(path)
    except Exception as e:
        print(e)
        return
    print(f"File ID: {_id}")


@app.command()
def get() -> None:
    factory = GetFilesFactory(
        "./src/config.yml"
    )
    injector = Injector(factory.configure)
    get_files_handler = injector.get(IGetFiles)
    try:
        feature_files = get_files_handler.run()
    except Exception as e:
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
    factory = DeleteFileFactory(
        "./src/config.yml"
    )
    injector = Injector(factory.configure)
    delete_file_handler = injector.get(IDeleteFile)
    try:
        _id = delete_file_handler.run(file_id)
    except Exception as e:
        print(e)
        return
    print(f"File ID: {_id}")


if __name__ == "__main__":
    app()
