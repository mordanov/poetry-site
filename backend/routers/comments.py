from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import Optional
from database import get_db
from routers.auth import get_current_admin
from models import Comment, Poem, Admin

router = APIRouter()

class CommentIn(BaseModel):
    author: Optional[str] = "Anonymous"
    body: str

@router.get("/{poem_id}")
def get_comments(poem_id: int, db: Session = Depends(get_db)):
    """Get all comments for a poem"""
    poem = db.query(Poem).filter(Poem.id == poem_id).first()
    if not poem:
        raise HTTPException(404, "Poem not found")

    comments = db.query(Comment).filter(Comment.poem_id == poem_id).order_by(Comment.created_at).all()

    result = []
    for comment in comments:
        result.append({
            "id": comment.id,
            "poem_id": comment.poem_id,
            "author": comment.author,
            "body": comment.body,
            "created_at": comment.created_at.isoformat()
        })

    return result

@router.post("/{poem_id}", status_code=201)
def add_comment(poem_id: int, data: CommentIn, db: Session = Depends(get_db)):
    """Add a comment to a poem"""
    poem = db.query(Poem).filter(Poem.id == poem_id).first()
    if not poem:
        raise HTTPException(404, "Poem not found")

    author = (data.author or "Anonymous").strip() or "Anonymous"

    comment = Comment(
        poem_id=poem_id,
        author=author,
        body=data.body.strip()
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return {
        "id": comment.id,
        "poem_id": comment.poem_id,
        "author": comment.author,
        "body": comment.body,
        "created_at": comment.created_at.isoformat()
    }

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Delete a comment (admin only)"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(404, "Comment not found")

    db.delete(comment)
    db.commit()

    return {"ok": True}

