from injector import inject
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.interface.session_handler import ISessionHandler
from domain.url_str import UrlStr
from infrastructure.model.base import Base


class SessionHandler(ISessionHandler):
    @inject
    def __init__(self, url: UrlStr) -> None:
        engine = create_engine(url.value, connect_args={"check_same_thread": False})
        self.session = sessionmaker(engine)
        Base.metadata.create_all(bind=engine)
