from fastapi import FastAPI

from app.database import engine
from app import models
from app.routers.students import router as students_router
from app.routers import attendance
from app.routers import recognition
from app.routers import users
from app.routers import auth
THRESHOLD = 0.8




models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart AI Campus Backend")

# 👇 ربط students router
app.include_router(students_router)
app.include_router(attendance.router)
app.include_router(recognition.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}




