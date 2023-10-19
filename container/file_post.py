from dependency_injector import containers, providers

from infrastructure.feature_file_repository import FeatureFileRepository
from infrastructure.session_handler import SessionHandler
from usecase.post_file import PostFile


class PostFileContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    session_handler = providers.Factory(SessionHandler, url=config.url)
    repository = providers.Factory(
        FeatureFileRepository, db=session_handler, repo_dir=config.repo_dir
    )
    post_file_handler = providers.Factory(PostFile, repo=repository)
