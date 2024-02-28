import os
import shutil

import sqlalchemy
from injector import inject

from domain.data_dir import DataDir
from domain.feature_data import FeatureData
from domain.interface.feature_data import IFeatureData
from domain.interface.feature_data_repository import IFeatureDataRepository
from domain.interface.session_handler import ISessionHandler
from infrastructure.error import ErrCode, RepositoryError
from infrastructure.model import models


class FeatureDataRepository(IFeatureDataRepository):
    @inject
    def __init__(self, db: ISessionHandler, repo_dir: DataDir) -> None:
        self.db = db
        self.repo_dir = repo_dir.value

    def save(self, feature_data: IFeatureData) -> str:
        try:
            with self.db.session.begin() as session:
                session.add(
                    models.FeatureData(
                        id=feature_data.file_id,
                        file_name=feature_data.file_name,
                        hash=feature_data.hash,
                        created_at=feature_data.created_at,
                    )
                )
        except sqlalchemy.exc.IntegrityError as e:
            raise RepositoryError(str(e), ErrCode.DUPLICATE_FILE)
        except Exception as e:
            raise RepositoryError(str(e))

        self.file_copy(feature_data)
        return feature_data.file_id

    def find(self, _id: str) -> FeatureData:
        try:
            with self.db.session() as session:
                result = (
                    session.query(models.FeatureData)
                    .filter(models.FeatureData.id == _id)
                    .first()
                )
        except Exception as e:
            raise RepositoryError(str(e))
        if result is None:
            raise RepositoryError(_id, ErrCode.NOT_FOUND)

        return FeatureData.from_rebuild(
            result.id,
            result.file_name,
            result.hash,
            result.created_at,
            f"{self.repo_dir}/{result.id}.csv",
        )

    def find_all(self) -> list[FeatureData]:
        try:
            with self.db.session() as session:
                result = session.query(models.FeatureData).all()
        except Exception as e:
            raise RepositoryError(str(e))

        return [
            FeatureData.from_rebuild(
                r.id, r.file_name, r.hash, r.created_at, f"{self.repo_dir}/{r.id}.csv"
            )
            for r in result
        ]

    def delete(self, _id: str) -> str:
        try:
            with self.db.session.begin() as session:
                result = (
                    session.query(models.FeatureData)
                    .filter(models.FeatureData.id == _id)
                    .first()
                )
                session.delete(result)
        except sqlalchemy.orm.exc.UnmappedInstanceError as e:
            raise RepositoryError(str(e), ErrCode.UNMAPPED_INSTANCE)
        except Exception as e:
            raise RepositoryError(str(e))

        self.file_delete(
            FeatureData.from_rebuild(
                result.id,
                result.file_name,
                result.hash,
                result.created_at,
                f"{self.repo_dir}/{result.id}.csv",
            )
        )
        return result.id

    def file_copy(self, feature_file: FeatureData) -> None:
        src_path = feature_file.src_path
        dst_path = f"{self.repo_dir}/{feature_file.file_id}.csv"
        shutil.copyfile(src_path, dst_path)

    def file_delete(self, feature_file: FeatureData) -> None:
        dst_path = f"{self.repo_dir}/{feature_file.file_id}.csv"
        os.remove(dst_path)
