from domain.interface.feature_file_repository import IFeatureFileRepository
from domain.interface.get_file import IGetFile
from domain.feature_file import FeatureFile


class GetFile(IGetFile):
    def __init__(self, repo: IFeatureFileRepository) -> None:
        self.repo = repo

    def run(self, _id: str) -> FeatureFile:
        return self.repo.find(_id)