from fastapi import APIRouter, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerPseudo, PlayerSaveData
from app.core.security import create_access_token, verify_token

router = APIRouter(prefix="", tags=["players"])

# === LECTURE DES DONNÉES DU JOUEUR ===
@router.get("/getdata/{user_id}")
def get_player_data(user_id: str, authorization: str = Header(None)):
    db: Session = SessionLocal()
    try:
        # Vérification du token
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")
        token = authorization.split(" ")[1]
        payload = verify_token(token)

        # Vérifie que le user_id du token correspond à celui demandé
        if payload["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")

        user = db.query(Player).filter(Player.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")

        return {
            "user_id": user.user_id,
            "username": user.username,
            "pseudo": user.pseudo,
            "coins": user.coins,
            "diamonds": user.diamonds,
            "level": user.level,
            "unlocked_characters": user.unlocked_characters,
            "spell_levels": user.spell_levels,
        }

    finally:
        db.close()


# === SAUVEGARDE DES DONNÉES ===
@router.post("/save")
def save_player_data(data: PlayerSaveData, authorization: str = Header(None)):
    db: Session = SessionLocal()
    try:
        # Vérification du token
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")
        token = authorization.split(" ")[1]
        payload = verify_token(token)

        # Vérifie que le joueur sauvegarde ses propres données
        if payload["user_id"] != data.user_id:
            raise HTTPException(status_code=403, detail="Tentative de triche détectée")

        user = db.query(Player).filter(Player.user_id == data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")

        user.coins = data.coins
        user.diamonds = data.diamonds
        user.level = data.level
        user.unlocked_characters = data.unlocked_characters
        user.spell_levels = data.spell_levels

        db.commit()
        return {"message": "✅ Données sauvegardées avec succès"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

    finally:
        db.close()


# === INSCRIPTION ===
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
        db.refresh(new_player)

        return {"message": "✅ Inscription réussie", "user_id": new_player.user_id}

    except Exception as e:
        db.rollback()
        print("❌ ERREUR REGISTER :", e)
        raise e

    finally:
        db.close()


# === CONNEXION ===
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

        token = create_access_token({"user_id": user.user_id, "username": user.username})
        return {"user_id": user.user_id, "access_token": token}

    finally:
        db.close()


# === CHANGEMENT DE PSEUDO ===
@router.post("/setnickname")
def set_nickname(data: PlayerPseudo):
    db: Session = SessionLocal()
    try:

        user = db.query(Player).filter(Player.user_id == data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")

        user.pseudo = data.pseudo
        db.commit()

        return {"message": f"✅ Pseudo '{data.pseudo}' enregistré pour {user.username}"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

    finally:
        db.close()
