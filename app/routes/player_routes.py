from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerPseudo

router = APIRouter(prefix="", tags=["players"])

# --- INSCRIPTION ---
@router.post("/register")
def register(player: PlayerCreate):
    db: Session = SessionLocal()
    try:
        existing = db.query(Player).filter(Player.username == player.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Nom déjà pris")

        new_player = Player(username=player.username, password=player.password)
        db.add(new_player)
        db.commit()

        return {"message": "✅ Inscription réussie"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

    finally:
        db.close()


# --- CONNEXION ---
@router.post("/login")
def login(player: PlayerCreate):
    db: Session = SessionLocal()
    try:
        user = (
            db.query(Player)
            .filter(Player.username == player.username, Player.password == player.password)
            .first()
        )

        if not user:
            raise HTTPException(status_code=401, detail="Identifiants invalides")

        return {"message": "✅ Connexion réussie", "player": user.username}

    finally:
        db.close()
        
# --- AJOUT / MODIFICATION DU PSEUDO ---
@router.post("/setnickname")
def set_nickname(data: PlayerPseudo):
    db: Session = SessionLocal()
    try:
        user = db.query(Player).filter(Player.username == data.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")

        user.pseudo = data.pseudo
        db.commit()

        return {"message": f"✅ Pseudo '{data.pseudo}' enregistré pour {data.username}"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

    finally:
        db.close()
