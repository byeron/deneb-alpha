from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.interface.session_handler import ISessionHandler
from infrastructure.model.base import Base


class SessionHandler(ISessionHandler):
    def __init__(self, url: str) -> None:
        engine = create_engine(url, connect_args={"check_same_thread": False})
        self.session = sessionmaker(engine)
        Base.metadata.create_all(bind=engine)
