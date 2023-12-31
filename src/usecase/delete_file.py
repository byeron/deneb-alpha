import shutil

from domain.interface.delete_file import IDeleteFile
from domain.interface.feature_data_repository import IFeatureDataRepository


class DeleteFile(IDeleteFile):
    def __init__(
        self, repo: IFeatureDataRepository, output_dir: str = "./src/medium"
    ) -> None:
        self.repo = repo
        self.output_dir = output_dir

    def run(self, _id: str) -> str:  # _id
        _id = self.repo.delete(_id)
        self._delete_directory(_id)
        return _id

    def _delete_directory(self, _id: str) -> None:
        shutil.rmtree(f"{self.output_dir}/{_id}")
