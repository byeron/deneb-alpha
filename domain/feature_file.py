import datetime
import hashlib
import os
import uuid
from dataclasses import dataclass

from domain.interface.feature_file import IFeatureFile


@dataclass(frozen=False)
class FeatureFile(IFeatureFile):
    _src_path: str
    _file_id: str = None
    _file_name: str = None
    _hash: str = None
    _created_at: str = None

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
        else:
            # 再構築の場合
            # バリデーションはしない
            pass

    @classmethod
    def from_new(cls, path: str):
        # 新規の構築の場合であることを明示してコンストラクタを呼び出す
        return cls(path)

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
    def src_path(self) -> str:
        return self._src_path

    @property
    def file_id(self) -> str:
        return self._file_id