from domain.interface.read_files import IReadFiles
from domain.interface.feature_file_repository import IFeatureFileRepository
from domain.feature_file import FeatureFile

class ReadFiles(IReadFiles):
    def __init__(self, repo: IFeatureFileRepository) -> None:
        self.repo = repo

    def run(self) -> list[FeatureFile]:
        return self.repo.find_all()