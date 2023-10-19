from domain.feature_file import FeatureFile
from domain.interface.create_file import ICreateFile
from domain.interface.feature_file_repository import IFeatureFileRepository


class CreateFile(ICreateFile):
    def __init__(self, repo: IFeatureFileRepository) -> None:
        self.repo = repo

    def run(self, path: str) -> str:  # _id
        feature_file = FeatureFile.from_new(path)
        _id = self.repo.save(feature_file)
        return _id
