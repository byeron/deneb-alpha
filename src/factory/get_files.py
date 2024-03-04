from domain.interface.get_files import IGetFiles
from usecase.get_files import GetFiles
from domain.url_str import UrlStr
from domain.data_dir import DataDir
from domain.interface.session_handler import ISessionHandler
from infrastructure.session_handler import SessionHandler
from domain.interface.feature_data_repository import IFeatureDataRepository
from infrastructure.feature_data_repository import FeatureDataRepository


import yaml
from injector import Module


class GetFilesFactory(Module):
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
        binder.bind(IGetFiles, to=GetFiles)
