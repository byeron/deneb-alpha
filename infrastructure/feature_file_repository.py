import os
import shutil

import sqlalchemy

from domain.feature_file import FeatureFile
from domain.interface.feature_file import IFeatureFile
from domain.interface.feature_file_repository import IFeatureFileRepository
from domain.interface.session_handler import ISessionHandler
from infrastructure.error import ErrCode, RepositoryError
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
        except sqlalchemy.exc.IntegrityError as e:
            raise RepositoryError(str(e), ErrCode.DUPLICATE_FILE)
        except Exception as e:
            raise RepositoryError(str(e))
        self.file_copy(feature_file)

        return feature_file.file_id

    def find(self, _id: str) -> FeatureFile:
        try:
            with self.db.session() as session:
                result = (
                    session.query(models.FeatureFile)
                    .filter(models.FeatureFile.id == _id)
                    .first()
                )
        except Exception as e:
            raise e

        return FeatureFile.from_rebuild(
            result.id, result.file_name, result.hash, result.created_at
        )

    def find_all(self) -> list[FeatureFile]:
        try:
            with self.db.session() as session:
                result = session.query(models.FeatureFile).all()
        except Exception as e:
            raise RepositoryError(str(e))

        return [
            FeatureFile.from_rebuild(r.id, r.file_name, r.hash, r.created_at)
            for r in result
        ]

    def delete(self, _id: str) -> str:
        try:
            with self.db.session.begin() as session:
                result = (
                    session.query(models.FeatureFile)
                    .filter(models.FeatureFile.id == _id)
                    .first()
                )
                session.delete(result)
        except sqlalchemy.orm.exc.UnmappedInstanceError as e:
            raise RepositoryError(str(e), ErrCode.UNMAPPED_INSTANCE)
        except Exception as e:
            raise RepositoryError(str(e))

        self.file_delete(
            FeatureFile.from_rebuild(
                result.id, result.file_name, result.hash, result.created_at
            )
        )
        return result.id

    def file_copy(self, feature_file: FeatureFile) -> None:
        src_path = feature_file.src_path
        dst_path = f"{self.repo_dir}/{feature_file.file_id}.csv"
        shutil.copyfile(src_path, dst_path)

    def file_delete(self, feature_file: FeatureFile) -> None:
        dst_path = f"{self.repo_dir}/{feature_file.file_id}.csv"
        os.remove(dst_path)
