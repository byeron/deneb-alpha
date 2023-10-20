from domain.interface.feature_data_repository import IFeatureDataRepository
from domain.interface.get_file import IGetFile
from domain.feature_data import FeatureData


class GetFile(IGetFile):
    def __init__(self, repo: IFeatureDataRepository) -> None:
        self.repo = repo

    def run(self, _id: str) -> FeatureData:
        return self.repo.find(_id)