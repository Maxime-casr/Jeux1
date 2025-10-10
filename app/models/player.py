from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    pseudo = Column(String, nullable=True)

