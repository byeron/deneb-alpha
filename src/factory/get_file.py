import yaml
from injector import Module

from domain.data_dir import DataDir
from domain.interface.feature_data_repository import IFeatureDataRepository
from domain.interface.get_file import IGetFile
from domain.interface.session_handler import ISessionHandler
from domain.url_str import UrlStr
from infrastructure.feature_data_repository import FeatureDataRepository
from infrastructure.session_handler import SessionHandler
from usecase.get_file import GetFile


class GetFileFactory(Module):
    def __init__(self, path="./src/config.yml"):
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        self.url = data["url"]
        self.dir = data["repo_dir"]

    def configure(self, binder):
        binder.bind(UrlStr, to=UrlStr(self.url))
        binder.bind(DataDir, to=DataDir(self.dir))
        binder.bind(ISessionHandler, to=SessionHandler)
        binder.bind(IFeatureDataRepository, to=FeatureDataRepository)
        binder.bind(IGetFile, GetFile)
