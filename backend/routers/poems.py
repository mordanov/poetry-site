from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from database import get_db
from routers.auth import get_current_admin
from models import Poem, Tag, Comment, Admin

router = APIRouter()

class PoemIn(BaseModel):
    title: Optional[str] = ""
    body: str
    tags: List[str] = []

class PoemUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = None

class PoemOut(BaseModel):
    id: int
    title: str
    body: str
    created_at: str
    updated_at: str
    tags: List[str]

    class Config:
        from_attributes = True

@router.get("")
def list_poems(tag: Optional[str] = None, db: Session = Depends(get_db)):
    """List all poems, optionally filtered by tag"""
    query = db.query(Poem).order_by(desc(Poem.created_at))

    if tag:
        query = query.join(Poem.tags).filter(Tag.name == tag.lower())

    poems = query.all()
    result = []
    for poem in poems:
        result.append({
            "id": poem.id,
            "title": poem.title,
            "body": poem.body,
            "created_at": poem.created_at.isoformat(),
            "updated_at": poem.updated_at.isoformat(),
            "tags": [t.name for t in poem.tags]
        })
    return result

@router.get("/tags")
def list_tags(db: Session = Depends(get_db)):
    """Get all tags with poem counts"""
    tags = db.query(Tag).all()
    result = []
    for tag in tags:
        count = db.query(func.count(Poem.id)).join(Poem.tags).filter(Tag.id == tag.id).scalar()
        result.append({"name": tag.name, "count": count})

    # Sort by count descending
    result.sort(key=lambda x: x["count"], reverse=True)
    return result

@router.get("/{poem_id}")
def get_poem(poem_id: int, db: Session = Depends(get_db)):
    """Get a specific poem"""
    poem = db.query(Poem).filter(Poem.id == poem_id).first()
    if not poem:
        raise HTTPException(404, "Poem not found")

    return {
        "id": poem.id,
        "title": poem.title,
        "body": poem.body,
        "created_at": poem.created_at.isoformat(),
        "updated_at": poem.updated_at.isoformat(),
        "tags": [t.name for t in poem.tags]
    }

@router.post("", status_code=201)
def create_poem(data: PoemIn, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Create a new poem"""
    poem = Poem(title=data.title, body=data.body)

    # Add tags
    for tag_name in data.tags:
        tag_name = tag_name.strip().lower()
        if tag_name:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()  # Get the tag ID
            poem.tags.append(tag)

    db.add(poem)
    db.commit()
    db.refresh(poem)

    return {
        "id": poem.id,
        "title": poem.title,
        "body": poem.body,
        "created_at": poem.created_at.isoformat(),
        "updated_at": poem.updated_at.isoformat(),
        "tags": [t.name for t in poem.tags]
    }

@router.put("/{poem_id}")
def update_poem(poem_id: int, data: PoemUpdate, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Update a poem"""
    poem = db.query(Poem).filter(Poem.id == poem_id).first()
    if not poem:
        raise HTTPException(404, "Poem not found")

    if data.title is not None:
        poem.title = data.title
    if data.body is not None:
        poem.body = data.body

    if data.tags is not None:
        # Replace tags
        poem.tags.clear()
        for tag_name in data.tags:
            tag_name = tag_name.strip().lower()
            if tag_name:
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.flush()
                poem.tags.append(tag)

    db.commit()
    db.refresh(poem)

    return {
        "id": poem.id,
        "title": poem.title,
        "body": poem.body,
        "created_at": poem.created_at.isoformat(),
        "updated_at": poem.updated_at.isoformat(),
        "tags": [t.name for t in poem.tags]
    }

@router.delete("/{poem_id}", status_code=204)
def delete_poem(poem_id: int, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Delete a poem"""
    poem = db.query(Poem).filter(Poem.id == poem_id).first()
    if not poem:
        raise HTTPException(404, "Poem not found")

    db.delete(poem)
    db.commit()


@router.get("/export/all")
def export_poems(admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Export all poems with tags to JSON format (admin only)"""
    poems = db.query(Poem).order_by(Poem.created_at).all()

    result = []
    for poem in poems:
        result.append({
            "title": poem.title,
            "body": poem.body,
            "tags": [t.name for t in poem.tags],
            "created_at": poem.created_at.isoformat(),
            "updated_at": poem.updated_at.isoformat()
        })

    return {
        "poems": result,
        "total": len(result),
        "exported_at": datetime.now().isoformat()
    }


@router.post("/import/all")
def import_poems(data: dict, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Import poems from JSON format (admin only)

    Expected format:
    {
        "poems": [
            {
                "title": "Poem title",
                "body": "Poem content",
                "tags": ["tag1", "tag2"]
            }
        ]
    }
    """
    if "poems" not in data or not isinstance(data["poems"], list):
        raise HTTPException(400, "Invalid format: 'poems' array is required")

    imported_count = 0
    errors = []

    for idx, poem_data in enumerate(data["poems"]):
        try:
            if "body" not in poem_data:
                errors.append(f"Poem #{idx + 1}: missing 'body' field")
                continue

            poem = Poem(
                title=poem_data.get("title", ""),
                body=poem_data["body"]
            )

            # Add tags if provided
            if "tags" in poem_data and isinstance(poem_data["tags"], list):
                for tag_name in poem_data["tags"]:
                    tag_name = tag_name.strip().lower()
                    if tag_name:
                        tag = db.query(Tag).filter(Tag.name == tag_name).first()
                        if not tag:
                            tag = Tag(name=tag_name)
                            db.add(tag)
                            db.flush()
                        poem.tags.append(tag)

            db.add(poem)
            imported_count += 1

        except Exception as e:
            errors.append(f"Poem #{idx + 1}: {str(e)}")

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Failed to save poems: {str(e)}")

    return {
        "imported": imported_count,
        "errors": errors,
        "total_attempted": len(data["poems"])
    }


@router.get("/export/comments")
def export_comments(admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Export all comments with associated poem info to JSON format (admin only)"""
    comments = db.query(Comment).order_by(Comment.created_at).all()

    result = []
    for comment in comments:
        poem = db.query(Poem).filter(Poem.id == comment.poem_id).first()
        result.append({
            "comment_id": comment.id,
            "author": comment.author,
            "body": comment.body,
            "created_at": comment.created_at.isoformat(),
            "poem": {
                "id": poem.id if poem else None,
                "title": poem.title if poem else "Deleted poem",
                "body_preview": poem.body[:100] + "..." if poem and len(poem.body) > 100 else (poem.body if poem else "")
            }
        })

    return {
        "comments": result,
        "total": len(result)
    }


