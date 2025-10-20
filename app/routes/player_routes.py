from fastapi import APIRouter, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.player import Player, Hero, HeroUnlocked, SpellLevel
from app.schemas.player import PlayerCreate, PlayerPseudo, PlayerSaveData
from app.core.security import create_access_token, verify_token

router = APIRouter(prefix="", tags=["players"])

@router.get("/getdata/{user_id}")
def get_player_data(user_id: str, authorization: str = Header(None)):
    db: Session = SessionLocal()
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")
        token = authorization.split(" ")[1]
        payload = verify_token(token)

        if payload["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")

        user = db.query(Player).filter(Player.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")

        # Récupération des héros débloqués
        unlocked_heroes = [
            h.hero.hero_id for h in user.heroes_unlocked
        ]

        # Récupération des sorts
        spells = [
            {"spell_id": s.spell_id, "spell_lvl": s.spell_lvl}
            for s in user.spells
        ]

        return {
            "user_id": user.user_id,
            "username": user.username,
            "pseudo": user.pseudo,
            "coins": user.coins,
            "diamonds": user.diamonds,
            "level": user.level,
            "unlocked_characters": unlocked_heroes,
            "spell_levels": spells
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

@router.post("/buy_character")
def buy_character(data: dict):
    db: Session = SessionLocal()
    try:
        user = db.query(Player).filter(Player.user_id == data["user_id"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")

        hero = db.query(Hero).filter(Hero.hero_id == data["character"]).first()
        if not hero:
            raise HTTPException(status_code=404, detail="Héros introuvable")

        already = (
            db.query(HeroUnlocked)
            .filter_by(user_id=user.user_id, hero_id=hero.hero_id)
            .first()
        )
        if already:
            return {"error": "already_unlocked"}

        if user.coins < hero.hero_prix:
            return {"error": "not_enough_coins"}

        # Ajout du héros débloqué
        user.coins -= hero.hero_prix
        new_unlock = HeroUnlocked(user_id=user.user_id, hero_id=hero.hero_id)
        db.add(new_unlock)
        db.commit()
        db.refresh(user)  # 👈 force la relation à se mettre à jour
        db.refresh(new_unlock)

        # Récupère les héros débloqués correctement après commit
        unlocked = [
            h.hero.hero_id for h in db.query(HeroUnlocked)
            .filter_by(user_id=user.user_id)
            .join(Hero)
            .all()
        ]

        return {
            "message": f"✅ {hero.hero_name} acheté pour {hero.hero_prix} pièces",
            "coins": user.coins,
            "unlocked_characters": unlocked,
        }

    except Exception as e:
        db.rollback()
        print("❌ ERREUR /buy_character :", e)
        raise HTTPException(status_code=500, detail=f"Erreur serveur : {str(e)}")
    finally:
        db.close()



