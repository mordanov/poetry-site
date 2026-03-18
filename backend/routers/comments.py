from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from typing import Optional
from database import get_db
from routers.auth import get_current_admin
from models import Comment, Poem, Admin

router = APIRouter()

class CommentIn(BaseModel):
    author: Optional[str] = "Anonymous"
    body: str

@router.get("/admin/all")
async def get_all_comments(admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Comment).join(Poem).order_by(desc(Comment.created_at))
    )
    comments = result.scalars().all()
    return [
        {
            "id": c.id,
            "poem_id": c.poem_id,
            "poem_uuid": c.poem.uuid,
            "poem_title": c.poem.title or "Untitled",
            "author": c.author,
            "body": c.body,
            "created_at": c.created_at.isoformat()
        }
        for c in comments
    ]

@router.get("/{poem_id}")
async def get_comments(poem_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Poem).where(Poem.id == poem_id))
    poem = result.scalar_one_or_none()
    if not poem:
        raise HTTPException(404, "Poem not found")

    result = await db.execute(
        select(Comment).where(Comment.poem_id == poem_id).order_by(Comment.created_at)
    )
    comments = result.scalars().all()
    return [
        {
            "id": c.id,
            "poem_id": c.poem_id,
            "author": c.author,
            "body": c.body,
            "created_at": c.created_at.isoformat()
        }
        for c in comments
    ]

@router.post("/{poem_id}", status_code=201)
async def add_comment(poem_id: int, data: CommentIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Poem).where(Poem.id == poem_id))
    poem = result.scalar_one_or_none()
    if not poem:
        raise HTTPException(404, "Poem not found")

    author = (data.author or "Anonymous").strip() or "Anonymous"
    comment = Comment(poem_id=poem_id, author=author, body=data.body.strip())
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    return {
        "id": comment.id,
        "poem_id": comment.poem_id,
        "author": comment.author,
        "body": comment.body,
        "created_at": comment.created_at.isoformat()
    }

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(404, "Comment not found")
    await db.delete(comment)
    await db.commit()
    return {"ok": True}
