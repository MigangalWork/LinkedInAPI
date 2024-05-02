from sqlalchemy import create_engine
from sqlalchemy.ext. declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.settings import Env

class DatabaseConnection:

    Base = declarative_base()

    def __init__(self) -> None:
        self.engine = create_engine(Env.DATABASE_HOST, connect_args={'check_same_thread': False})
        self.session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base.metadata.create_all(self.engine)

    def create_session(self):
        return self.session_factory()