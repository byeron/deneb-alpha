from infrastructure.feature_data_repository import FeatureDataRepository
from infrastructure.session_handler import SessionHandler
from usecase.get_file import GetFile
from domain.interface.feature_data_repository import IFeatureDataRepository
from domain.interface.session_handler import ISessionHandler
import yaml
from domain.interface.get_file import IGetFile
from domain.data_dir import DataDir
from domain.url_str import UrlStr
from injector import Module


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
