from sqlalchemy import create_engine
from sqlalchemy.ext. declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.settings import Env

class DatabaseConnection:

    Base = declarative_base()

    @classmethod
    def main_database_connection(cls) -> None:
        cls.engine = create_engine(Env.DATABASE_HOST, connect_args={'check_same_thread': False})
        cls.session_factory = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        cls.Base.metadata.create_all(bind=cls.engine)

    @classmethod
    def create_session(cls):
        return cls.session_factory()
    
