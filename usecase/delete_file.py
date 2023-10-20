from domain.interface.delete_file import IDeleteFile
from domain.interface.feature_data_repository import IFeatureDataRepository


class DeleteFile(IDeleteFile):
    def __init__(self, repo: IFeatureDataRepository) -> None:
        self.repo = repo

    def run(self, _id: str) -> str:  # _id
        _id = self.repo.delete(_id)
        return _id
