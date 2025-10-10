from fastapi import FastAPI
from app.routes import player_routes

app = FastAPI(title="API du jeu Unity")

# Inclure les routes
app.include_router(player_routes.router)


