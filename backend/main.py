from fastapi import FastAPI
from core.config import settings

app = FastAPI(title=settings.PROJECT_TITLE, description=settings.PROJECT_DESCRIPTION, version=settings.PROJECT_VERSION)

@app.get("/")
def hello():
    return {"message": "Hello FASTAPI 🚀"}