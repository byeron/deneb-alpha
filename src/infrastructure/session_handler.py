from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.interface.session_handler import ISessionHandler
from infrastructure.model.base import Base
from domain.url_str import UrlStr
from injector import inject


class SessionHandler(ISessionHandler):
    @inject
    def __init__(self, url: UrlStr) -> None:
        engine = create_engine(url.value, connect_args={"check_same_thread": False})
        self.session = sessionmaker(engine)
        Base.metadata.create_all(bind=engine)
