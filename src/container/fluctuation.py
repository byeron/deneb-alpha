from dependency_injector import containers, providers

from domain.ftest_config import FtestConfig
from domain.multipletest_config import MultipletestConfig
from usecase.ftest import Ftest
from usecase.multipletest import Multipletest


class FtestContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    fluctuation_config = providers.Factory(
        FtestConfig,
        control=config.control,
        experiment=config.experiment,
        alpha=config.alpha,
    )
    fluctuation_handler = providers.Factory(Ftest, config=fluctuation_config)


class MultipletestContiner(containers.DeclarativeContainer):
    config = providers.Configuration()
    multipletest_config = providers.Factory(
        MultipletestConfig, method=config.method, alpha=config.alpha
    )
    multipletest_handler = providers.Factory(Multipletest, config=multipletest_config)
