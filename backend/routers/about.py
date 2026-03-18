from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from database import get_db
from routers.auth import get_current_admin
from models import About, Admin

router = APIRouter()

class AboutUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None

@router.get("")
async def get_about(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(About).where(About.id == 1))
    about = result.scalar_one_or_none()
    if not about:
        return {}
    return {
        "id": about.id,
        "name": about.name,
        "bio": about.bio,
        "photo_url": about.photo_url,
        "updated_at": about.updated_at.isoformat() if about.updated_at else None
    }

@router.put("")
async def update_about(data: AboutUpdate, admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(About).where(About.id == 1))
    about = result.scalar_one_or_none()
    if not about:
        about = About(id=1)
        db.add(about)

    if data.name is not None:
        about.name = data.name
    if data.bio is not None:
        about.bio = data.bio
    if data.photo_url is not None:
        about.photo_url = data.photo_url

    await db.commit()
    await db.refresh(about)

    return {
        "id": about.id,
        "name": about.name,
        "bio": about.bio,
        "photo_url": about.photo_url,
        "updated_at": about.updated_at.isoformat() if about.updated_at else None
    }
