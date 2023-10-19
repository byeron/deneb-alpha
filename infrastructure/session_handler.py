from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.interface.session_handler import ISessionHandler


class SessionHandler(ISessionHandler):
    def __init__(self, url: str) -> None:
        engine = create_engine(url)
        self.session = sessionmaker(engine)