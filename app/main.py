from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# from app.database import Base, engine
from app.routes import users, calculations, auth

app = FastAPI()

# Static frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/register")
def serve_register():
    return FileResponse(os.path.join("frontend", "register.html"))

@app.get("/login")
def serve_login():
    return FileResponse(os.path.join("frontend", "login.html"))

# Simple health check 
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse(os.path.join("frontend", "dashboard.html"))

# API routers
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(calculations.router, prefix="/api", tags=["Calculations"])
app.include_router(auth.router, prefix="/api", tags=["Auth"])
