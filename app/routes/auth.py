# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from app import models, schemas, database
from app.schemas import UserLogin
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-secret-key"  # TODO: env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    try:
        hashed = hash_password(user.password)
        db_user = models.User(username=user.username, email=user.email, hashed_password=hashed)
        db.add(db_user); db.commit(); db.refresh(db_user)
        return "Registration successful!"
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or username already in use")

@router.post("/login")
def login(credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": user.email})
    response.set_cookie("access_token", token, httponly=True, samesite="lax", secure=False,
                        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    response.headers["X-Access-Token"] = token
    return "Login successful!"

def _get_token(request: Request) -> Optional[str]:
    return request.cookies.get("access_token") or (
        request.headers.get("Authorization", "").split(" ", 1)[1].strip()
        if request.headers.get("Authorization", "").lower().startswith("bearer ")
        else None
    )

def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.User:
    token = _get_token(request)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
