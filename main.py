from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Smart AI Campus")

app.include_router(router)