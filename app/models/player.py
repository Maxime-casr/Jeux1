from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
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


    spells = relationship("SpellLevel", back_populates="player", cascade="all, delete-orphan")
    heroes_unlocked = relationship("HeroUnlocked",back_populates="player",cascade="all, delete-orphan")
    
class HeroUnlocked(Base):
    __tablename__ = "hero_unlocked"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("players.user_id"), nullable=False, index=True)
    hero_id = Column(String, ForeignKey("hero.hero_id"), nullable=False, index=True)

    # Relations ORM
    player = relationship("Player", back_populates="heroes_unlocked")
    hero = relationship("Hero")


class SpellLevel(Base):
    __tablename__ = "spell_levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("players.user_id"), nullable=False, index=True)
    spell_id = Column(String, nullable=False, index=True)
    spell_lvl = Column(Integer, default=1)

    player = relationship("Player", back_populates="spells")


class Hero(Base):
    __tablename__ = "hero"

    id = Column(Integer, primary_key=True, index=True)
    hero_id = Column(String, unique=True, nullable=False)
    hero_name = Column(String, nullable=True)
    hero_prix = Column(Integer, default=0)

    

