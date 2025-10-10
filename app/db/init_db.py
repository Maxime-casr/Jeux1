from app.db.session import engine
from app.models.player import Base

def init_db():
    print("⚠️ Suppression de toutes les tables existantes...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables supprimées.")

    print("🛠️ Création des tables à neuf...")
    Base.metadata.create_all(bind=engine)
    print("✅ Nouvelles tables créées avec succès !")

if __name__ == "__main__":
    init_db()

