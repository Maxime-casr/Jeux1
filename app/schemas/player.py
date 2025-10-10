from pydantic import BaseModel

class PlayerCreate(BaseModel):
    username: str
    password: str

class PlayerLogin(BaseModel):
    username: str
    password: str
    
class PlayerPseudo(BaseModel):
    username: str
    pseudo: str
