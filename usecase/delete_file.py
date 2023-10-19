from domain.interface.delete_file import IDeleteFile
from domain.interface.feature_file_repository import IFeatureFileRepository


class DeleteFile(IDeleteFile):
    def __init__(self, repo: IFeatureFileRepository) -> None:
        self.repo = repo

    def run(self, _id: str) -> str:  # _id
        _id = self.repo.delete(_id)
        return _id
