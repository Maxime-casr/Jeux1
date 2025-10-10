from pydantic import BaseModel

class PlayerCreate(BaseModel):
    username: str
    password: str

class PlayerLogin(BaseModel):
    username: str
    password: str
    
class PlayerPseudo(BaseModel):
    user_id: str
    pseudo: str

