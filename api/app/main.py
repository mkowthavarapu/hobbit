from fastapi import FastAPI
from app.routes import user

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(user.router, prefix="/api/v1")
