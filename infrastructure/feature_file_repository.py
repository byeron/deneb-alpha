import os
import shutil

from domain.feature_file import FeatureFile
from domain.interface.feature_file import IFeatureFile
from domain.interface.feature_file_repository import IFeatureFileRepository
from domain.interface.session_handler import ISessionHandler
from infrastructure.model import models


class FeatureFileRepository(IFeatureFileRepository):
    def __init__(self, db: ISessionHandler, repo_dir: str) -> None:
        self.db = db
        self.repo_dir = repo_dir

    def save(self, feature_file: IFeatureFile) -> str:
        try:
            with self.db.session.begin() as session:
                session.add(
                    models.FeatureFile(
                        id=feature_file.file_id,
                        file_name=feature_file.file_name,
                        hash=feature_file.hash,
                        created_at=feature_file.created_at,
                    )
                )
        except Exception as e:
            raise e
        self.file_copy(feature_file)

        return feature_file.file_id

    def find(self, _id: str) -> FeatureFile:
        try:
            with self.db.session.begin() as session:
                result = self.db.session.query(FeatureFile).filter_by(id=_id).first()
        except Exception as e:
            raise e

        return FeatureFile(result.id, result.path, result.created_at, result.updated_at)

    def file_copy(self, feature_file: IFeatureFile) -> None:
        src_path = feature_file.src_path
        dst_path = f"{self.repo_dir}/{feature_file.file_id}.csv"
        shutil.copyfile(src_path, dst_path)

    def file_delete(self, feature_file: IFeatureFile) -> None:
        dst_path = f"{self.repo_dir}/{feature_file.file_id}.csv"
        os.remove(dst_path)
