from sqlalchemy import Column, Integer, String, JSON
from app.db.base import Base
import uuid

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    pseudo = Column(String, nullable=True)
    
    coins = Column(Integer, default=0)
    diamonds = Column(Integer, default=0)
    level = Column(Integer, default=1)
    
    unlocked_characters = Column(JSON, default=list)
    spell_levels = Column(JSON, default = list)


