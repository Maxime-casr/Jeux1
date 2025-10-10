from app.db.session import engine
from app.models.player import Base

def init_db():
    print("🛠️ Création des tables si elles n'existent pas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées ou déjà existantes.")

if __name__ == "__main__":
    init_db()
