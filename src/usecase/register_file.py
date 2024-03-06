import os

from domain.feature_data import FeatureData
from domain.interface.feature_data_repository import IFeatureDataRepository
from domain.interface.register_file import IRegisterFile
from injector import inject
from domain.output_dir import OutputDir


class RegisterFile(IRegisterFile):
    @inject
    def __init__(
        self, repo: IFeatureDataRepository, output_dir: OutputDir
    ) -> None:
        self.repo = repo
        self.output_dir = output_dir

    def run(self, path: str) -> str:  # _id
        feature_file = FeatureData.from_new(path)
        _id = self.repo.save(feature_file)
        self._create_directory(_id)
        return _id

    def _create_directory(self, _id: str) -> None:
        print(self.output_dir)
        os.makedirs(f"{self.output_dir.value}/{_id}", exist_ok=True)
