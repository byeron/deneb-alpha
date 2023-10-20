from domain.feature_data import FeatureData
from domain.interface.register_file import IRegisterFile
from domain.interface.feature_data_repository import IFeatureDataRepository


class RegisterFile(IRegisterFile):
    def __init__(self, repo: IFeatureDataRepository) -> None:
        self.repo = repo

    def run(self, path: str) -> str:  # _id
        feature_file = FeatureData.from_new(path)
        _id = self.repo.save(feature_file)
        return _id
