from datetime import datetime, timedelta
from typing import Optional
import os

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from sqlmodel import Session, select

from ..db import get_session
from ..models import User, UserRole
from .dependencies import get_current_user

from ..config import get_settings

settings = get_settings()
SECRET_KEY = settings.SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.VOLUNTEER


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=Token)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(email=user.email, hashed_password=get_password_hash(user.password), role=user.role)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    access_token = create_access_token({"sub": str(db_user.id), "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == credentials.email)).first()
    if not db_user or not verify_password(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(db_user.id), "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def read_me(current=Depends(get_current_user)):
    """Return the currently authenticated user."""
    return current
