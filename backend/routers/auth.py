from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from database import get_db
from models import Admin

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_admin(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        result = await db.execute(select(Admin).where(Admin.username == username))
        admin = result.scalar_one_or_none()
        if not admin:
            raise HTTPException(status_code=401, detail="User not found")
        return admin
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_optional_admin(token: Optional[str] = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """Get admin if token is valid, otherwise return None"""
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            return None
        result = await db.execute(select(Admin).where(Admin.username == username))
        return result.scalar_one_or_none()
    except:
        return None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admin).where(Admin.username == form.username))
    admin = result.scalar_one_or_none()
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not bcrypt.checkpw(form.password.encode(), admin.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(admin.username)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def me(admin: Admin = Depends(get_current_admin)):
    return {"username": admin.username}

@router.post("/change-password")
async def change_password(data: PasswordChange, admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    if not bcrypt.checkpw(data.current_password.encode(), admin.password_hash.encode()):
        raise HTTPException(status_code=400, detail="Current password is wrong")
    new_hash = bcrypt.hashpw(data.new_password.encode(), bcrypt.gensalt()).decode()
    admin.password_hash = new_hash
    await db.commit()
    return {"ok": True}
