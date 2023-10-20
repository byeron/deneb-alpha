from dependency_injector import containers, providers

from infrastructure.feature_data_repository import FeatureDataRepository
from infrastructure.session_handler import SessionHandler
from usecase.register_file import RegisterFile


class RegisterFileContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    session_handler = providers.Factory(SessionHandler, url=config.url)
    repository = providers.Factory(
        FeatureDataRepository, db=session_handler, repo_dir=config.repo_dir
    )
    handler = providers.Factory(RegisterFile, repo=repository)
