from enum import IntEnum, auto


class ErrCode(IntEnum):
    UNMAPPED_INSTANCE = auto()
    DUPLICATE_FILE = auto()


class RepositoryError(Exception):
    def __init__(self, message: str, err_code: int = 0) -> None:
        self.message = ""

        match err_code:
            case ErrCode.UNMAPPED_INSTANCE:
                self.message = (
                    f"Repository Error: The File ID is not found.\n{message}."
                )
            case ErrCode.DUPLICATE_FILE:
                self.message = (
                    f"Repository Error: The File is already exists\n{message}."
                )
            case _:
                self.message = f"Repository Error: {message}"

    def __str__(self) -> str:
        return self.message
