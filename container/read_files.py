from dependency_injector import containers, providers

from infrastructure.feature_file_repository import FeatureFileRepository
from infrastructure.session_handler import SessionHandler
from usecase.read_files import ReadFiles


class ReadFilesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    session_handler = providers.Factory(SessionHandler, url=config.url)
    repository = providers.Factory(
        FeatureFileRepository, db=session_handler, repo_dir=config.repo_dir
    )
    read_files_handler = providers.Factory(ReadFiles, repo=repository)
