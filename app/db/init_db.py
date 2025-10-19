from app.db.session import engine, SessionLocal
from app.models.player import Base, Hero

def init_db():
    print("⚠️ Suppression de toutes les tables existantes...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables supprimées.")

    print("🛠️ Création des tables à neuf...")
    Base.metadata.create_all(bind=engine)
    print("✅ Nouvelles tables créées avec succès !")

    # === Ajout automatique des héros de base ===
    db = SessionLocal()
    try:
        print("🧩 Insertion des héros par défaut...")

        default_heroes = [
            Hero(hero_id="Mage", hero_name="Mage", hero_prix=500),
            Hero(hero_id="Chevalier", hero_name="Chevalier", hero_prix=750),
            Hero(hero_id="Bucheron", hero_name="bucheron", hero_prix=1000),
            Hero(hero_id="Infamite", hero_name="Infamite", hero_prix=5000),
        ]

        db.add_all(default_heroes)
        db.commit()

        print("✅ Héros ajoutés avec succès dans la base !")
    except Exception as e:
        print("❌ Erreur lors de l'ajout des héros :", e)
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
