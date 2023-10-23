import datetime
import hashlib
import os
import uuid
from dataclasses import dataclass

import pandas as pd

from domain.interface.feature_data import IFeatureData


@dataclass(frozen=False)
class FeatureData(IFeatureData):
    _src_path: str
    _file_id: str = None
    _file_name: str = None
    _hash: str = None
    _created_at: str = None
    _matrix: pd.DataFrame = None
    _fluctuation: pd.DataFrame = None

    def __post_init__(self):
        if self._src_path is not None:
            # 初めてのファイルの場合
            if not os.path.exists(self._src_path):
                raise FileNotFoundError(f"File not found: {self._src_path}")

            # validate matrix
            is_ok, msg = self._validate_matrix()
            if not is_ok:
                raise ValueError(msg)

            # 各メンバ変数を設定
            # set _file_id
            if self._file_id is None:
                self._file_id = str(uuid.uuid4())

            # get _file_name & set _file_name
            self._file_name = os.path.basename(self._src_path).split(".")[0]

            # calculate file hash & set hash
            self._hash = self._calc_hash()

            # set created_at
            now = datetime.datetime.now()
            self._created_at = now.strftime("%Y-%m-%d %H:%M:%S")

            # set matrix
            self._matrix = pd.read_csv(
                self._src_path, index_col=0, header=0, encoding="utf-8"
            )
        else:
            # 再構築の場合
            # バリデーションはしない
            pass

    @classmethod
    def from_new(cls, path: str):
        # 新規の構築の場合であることを明示してコンストラクタを呼び出す
        return cls(path)

    @classmethod
    def from_rebuild(
        cls, file_id: str, file_name: str, hash: str, created_at: str, path: str
    ):
        # 再構築の場合であることを明示してコンストラクタを呼び出す
        df = pd.read_csv(path, index_col=0, header=0, encoding="utf-8")
        return cls(None, file_id, file_name, hash, created_at, df)

    def _validate_matrix(self) -> (bool, str):
        return (True, None)  # TODO: implement

    def _calc_hash(self) -> str:
        hash_md5 = hashlib.md5()
        with open(self._src_path, "rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                hash_md5.update(byte_block)
        return hash_md5.hexdigest()

    @property
    def fluctuation(self) -> pd.DataFrame:
        return self._fluctuation

    @fluctuation.setter
    def fluctuation(self, reject: list[bool]):
        reject = self._matrix.columns[reject]
        self._fluctuation = self._matrix.loc[:, reject]
        return self._fluctuation

    @property
    def src_path(self) -> str:
        return self._src_path

    @property
    def file_id(self) -> str:
        return self._file_id

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def matrix(self) -> pd.DataFrame:
        return self._matrix
