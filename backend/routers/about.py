from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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
def get_about(db: Session = Depends(get_db)):
    """Get about page information"""
    about = db.query(About).filter(About.id == 1).first()
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
def update_about(data: AboutUpdate, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Update about page information"""
    about = db.query(About).filter(About.id == 1).first()
    if not about:
        about = About(id=1)
        db.add(about)

    if data.name is not None:
        about.name = data.name
    if data.bio is not None:
        about.bio = data.bio
    if data.photo_url is not None:
        about.photo_url = data.photo_url

    db.commit()
    db.refresh(about)

    return {
        "id": about.id,
        "name": about.name,
        "bio": about.bio,
        "photo_url": about.photo_url,
        "updated_at": about.updated_at.isoformat() if about.updated_at else None
    }

