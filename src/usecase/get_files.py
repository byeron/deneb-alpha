from domain.feature_data import FeatureData
from domain.interface.feature_data_repository import IFeatureDataRepository
from domain.interface.get_files import IGetFiles
from injector import inject


class GetFiles(IGetFiles):
    @inject
    def __init__(self, repo: IFeatureDataRepository) -> None:
        self.repo = repo

    def run(self) -> list[FeatureData]:
        return self.repo.find_all()
