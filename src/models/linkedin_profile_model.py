from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from pytz import UTC
from src.db_connection.database import DatabaseConnection


class Profile(DatabaseConnection.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    last_description = Column(String, default='')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), 
                        onupdate=datetime.now(UTC))


