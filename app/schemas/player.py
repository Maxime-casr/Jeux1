from pydantic import BaseModel
from typing import List, Dict

class PlayerCreate(BaseModel):
    username: str
    password: str

class PlayerLogin(BaseModel):
    username: str
    password: str
    
class PlayerPseudo(BaseModel):
    user_id: str
    pseudo: str

class PlayerSaveData(BaseModel):
    user_id: str
    coins: int
    diamonds: int
    level: int
    unlocked_characters: List[str]
    spell_levels: List[Dict]
