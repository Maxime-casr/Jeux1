from app.db.session import engine, SessionLocal
from app.models.player import Base, Hero, Spell

def init_db():
    print("⚠️ Suppression de toutes les tables existantes...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables supprimées.")

    print("🛠️ Création des tables à neuf...")
    Base.metadata.create_all(bind=engine)
    print("✅ Nouvelles tables créées avec succès !")

    db = SessionLocal()
    try:
        print("🧩 Insertion des héros et sorts par défaut...")

        default_heroes = [
            Hero(hero_id="Mage", hero_name="Mage", hero_prix=500),
            Hero(hero_id="Chevalier", hero_name="Chevalier", hero_prix=750),
            Hero(hero_id="Bucheron", hero_name="Bucheron", hero_prix=1000),
            Hero(hero_id="Infamite", hero_name="Infamite", hero_prix=5000),
        ]

        heroes_spells = {
            "Chevalier": [
                ("CbnChe", "Cabane de guerrier"),
                ("Cp_epee", "Coup d'épée"),
                ("DnnBouc", "Armure"),
                ("Duel", "Duel"),
                ("Bouc", "Provocation"),
                ("Rush", "Rush"),
            ],
            "Mage": [
                ("Bouledefeu", "Boule de feu"),
                ("implosion", "Implosion"),
                ("Temp", "Tempête"),
                ("Tor", "Tornade"),
                ("totem", "Totem"),
                ("trance", "trsd"),
            ],
        }

        default_spells = []
        for hero_id, spells in heroes_spells.items():
            for spell_id, spell_name in spells:
                default_spells.append(
                    Spell(spell_id=spell_id, hero_id=hero_id, spell_name=spell_name, spell_de_base=True)
                )


        db.add_all(default_heroes + default_spells)
        db.commit()

        print("✅ Héros et sorts ajoutés avec succès dans la base !")

    except Exception as e:
        print("❌ Erreur lors de l'ajout :", e)
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()

