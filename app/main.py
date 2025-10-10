from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Charger les variables du fichier .env

app = FastAPI()

# Connexion à la base PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

# Schéma pour les requêtes
class Player(BaseModel):
    username: str
    password: str

# ROUTE: inscription
@app.post("/register")
def register(player: Player):
    conn = get_connection()
    cur = conn.cursor()

    # Vérifier si l'utilisateur existe déjà
    cur.execute("SELECT * FROM players WHERE username = %s", (player.username,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Nom déjà pris")

    # Insérer le nouveau joueur
    cur.execute("INSERT INTO players (username, password) VALUES (%s, %s)", (player.username, player.password))
    conn.commit()
    conn.close()

    return {"message": "Inscription réussie"}

# ROUTE: connexion
@app.post("/login")
def login(player: Player):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM players WHERE username = %s AND password = %s", (player.username, player.password))
    result = cur.fetchone()
    conn.close()

    if result:
        return {"message": "Connexion réussie", "player": player.username}
    else:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
