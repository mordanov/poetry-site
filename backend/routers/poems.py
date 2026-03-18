from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from database import get_db
from routers.auth import get_current_admin, get_optional_admin
from models import Poem, Tag, Comment, Admin, PoemVersion
import io
import json
import os
import zipfile
import sys
import traceback

router = APIRouter()

UPLOADS_DIR = os.getenv("UPLOADS_DIR", "/app/data/uploads/poems")
MAX_IMAGE_SIZE = 1 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg": ".jpg", "image/png": ".png"}

class PoemIn(BaseModel):
    title: Optional[str] = ""
    body: str
    tags: List[str] = []
    is_draft: int = 0

class PoemUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = None
    is_draft: Optional[int] = None

class PoemOut(BaseModel):
    id: int
    uuid: str
    title: str
    body: str
    image_url: Optional[str]
    is_draft: int
    created_at: str
    updated_at: str
    tags: List[str]
    comment_count: Optional[int] = None

    class Config:
        from_attributes = True

def _image_url(poem: Poem) -> Optional[str]:
    if not poem.image_filename:
        return None
    return f"/uploads/poems/{poem.image_filename}"

def _poem_to_dict(poem: Poem, comment_count: Optional[int] = None) -> dict:
    payload = {
        "id": poem.id,
        "uuid": poem.uuid,
        "title": poem.title,
        "body": poem.body,
        "image_url": _image_url(poem),
        "is_draft": int(poem.is_draft) if poem.is_draft is not None else 0,
        "created_at": poem.created_at.isoformat(),
        "updated_at": poem.updated_at.isoformat(),
        "tags": [t.name for t in poem.tags]
    }
    if comment_count is not None:
        payload["comment_count"] = comment_count
    return payload

async def _get_or_create_tag(db: AsyncSession, name: str) -> Tag:
    result = await db.execute(select(Tag).where(Tag.name == name))
    tag = result.scalar_one_or_none()
    if not tag:
        tag = Tag(name=name)
        db.add(tag)
        await db.flush()
    return tag

# ====== LIST & FILTER ======
@router.get("")
async def list_poems(
    tag: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    admin: Optional[Admin] = Depends(get_optional_admin),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Poem).options(selectinload(Poem.tags))
    if admin:
        stmt = stmt.order_by(desc(Poem.is_draft), desc(Poem.created_at))
    else:
        stmt = stmt.where(Poem.is_draft == False).order_by(desc(Poem.created_at))

    if tag:
        stmt = stmt.join(Poem.tags).where(Tag.name == tag.lower())

    total_result = await db.execute(select(func.count()).select_from(stmt.subquery()))
    total = total_result.scalar_one()

    offset = (page - 1) * limit
    result = await db.execute(stmt.offset(offset).limit(limit))
    poems = result.scalars().all()

    poem_ids = [p.id for p in poems]
    comment_counts = {}
    if poem_ids:
        cc_result = await db.execute(
            select(Comment.poem_id, func.count(Comment.id))
            .where(Comment.poem_id.in_(poem_ids))
            .group_by(Comment.poem_id)
        )
        comment_counts = dict(cc_result.all())

    return {
        "poems": [_poem_to_dict(p, comment_counts.get(p.id, 0)) for p in poems],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }

@router.get("/tags")
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).options(selectinload(Tag.poems)))
    tags = result.scalars().all()
    out = [{"name": t.name, "count": len(t.poems)} for t in tags if len(t.poems) > 0]
    out.sort(key=lambda x: x["count"], reverse=True)
    return out

# ====== SPECIAL ROUTES (before {poem_id}) ======
@router.get("/uuid/{poem_uuid}")
async def get_poem_by_uuid(poem_uuid: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Poem).options(selectinload(Poem.tags)).where(Poem.uuid == poem_uuid)
    )
    poem = result.scalar_one_or_none()
    if not poem:
        raise HTTPException(404, "Poem not found")
    return _poem_to_dict(poem)

@router.get("/export/poems")
async def export_poems(admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Poem).options(selectinload(Poem.tags), selectinload(Poem.comments)).order_by(Poem.uuid)
    )
    poems = result.scalars().all()

    poems_payload = []
    comments_payload = []

    for poem in poems:
        poems_payload.append({
            "uuid": poem.uuid,
            "title": poem.title,
            "body": poem.body,
            "tags": [t.name for t in poem.tags],
            "image_filename": poem.image_filename,
            "is_draft": int(poem.is_draft) if poem.is_draft is not None else 0,
            "created_at": poem.created_at.isoformat(),
            "updated_at": poem.updated_at.isoformat()
        })
        for comment in poem.comments:
            comments_payload.append({
                "poem_uuid": poem.uuid,
                "author": comment.author,
                "body": comment.body,
                "created_at": comment.created_at.isoformat()
            })

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr("poems.json", json.dumps({
            "poems": poems_payload,
            "total": len(poems_payload),
            "exported_at": datetime.now().isoformat()
        }, ensure_ascii=False, indent=2))
        zipf.writestr("comments.json", json.dumps({
            "comments": comments_payload,
            "total": len(comments_payload),
            "exported_at": datetime.now().isoformat()
        }, ensure_ascii=False, indent=2))
        for poem in poems:
            if poem.image_filename:
                image_path = os.path.join(UPLOADS_DIR, poem.image_filename)
                if os.path.exists(image_path):
                    zipf.write(image_path, f"images/{poem.image_filename}")

    buffer.seek(0)
    filename = f"poems-export-{datetime.now().strftime('%Y-%m-%d')}.zip"
    return StreamingResponse(buffer, media_type="application/zip",
                             headers={"Content-Disposition": f"attachment; filename={filename}"})

@router.post("/import")
async def import_poems(file: UploadFile = File(...), admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(400, "Invalid file format: expected .zip")

    content = await file.read()
    buffer = io.BytesIO(content)

    try:
        with zipfile.ZipFile(buffer, "r") as zipf:
            if "poems.json" not in zipf.namelist():
                raise HTTPException(400, "Invalid archive: poems.json not found")

            poems_data = json.loads(zipf.read("poems.json").decode("utf-8"))
            if "poems" not in poems_data or not isinstance(poems_data["poems"], list):
                raise HTTPException(400, "Invalid format: 'poems' array is required")

            imported_poems = 0
            imported_comments = 0
            errors = []
            uuid_to_poem_id = {}

            for idx, poem_data in enumerate(poems_data["poems"]):
                try:
                    if "body" not in poem_data:
                        errors.append(f"Poem #{idx + 1}: missing 'body' field")
                        continue

                    poem_uuid = poem_data.get("uuid")
                    if not poem_uuid:
                        errors.append(f"Poem #{idx + 1}: missing 'uuid' field")
                        continue

                    existing = await db.execute(select(Poem).where(Poem.uuid == poem_uuid))
                    if existing.scalar_one_or_none():
                        errors.append(f"Poem #{idx + 1}: uuid already exists")
                        uuid_to_poem_id[poem_uuid] = existing.scalar_one_or_none().id if existing.scalar_one_or_none() else None
                        continue

                    poem = Poem(
                        uuid=poem_uuid,
                        title=poem_data.get("title", ""),
                        body=poem_data["body"],
                        is_draft=bool(poem_data.get("is_draft", 0)),
                        created_at=datetime.fromisoformat(poem_data["created_at"]) if poem_data.get("created_at") else datetime.utcnow(),
                        updated_at=datetime.fromisoformat(poem_data["updated_at"]) if poem_data.get("updated_at") else datetime.utcnow(),
                    )

                    for tag_name in poem_data.get("tags", []):
                        tag_name = tag_name.strip().lower()
                        if tag_name:
                            poem.tags.append(await _get_or_create_tag(db, tag_name))

                    image_filename = poem_data.get("image_filename")
                    if image_filename:
                        image_entry = f"images/{image_filename}"
                        if image_entry in zipf.namelist():
                            ext = os.path.splitext(image_filename)[1].lower()
                            if ext in (".jpg", ".jpeg", ".png"):
                                target = f"{poem.uuid}{'.png' if ext == '.png' else '.jpg'}"
                                os.makedirs(UPLOADS_DIR, exist_ok=True)
                                image_bytes = zipf.read(image_entry)
                                if len(image_bytes) <= MAX_IMAGE_SIZE:
                                    with open(os.path.join(UPLOADS_DIR, target), "wb") as f:
                                        f.write(image_bytes)
                                    poem.image_filename = target

                    db.add(poem)
                    await db.flush()
                    uuid_to_poem_id[poem_uuid] = poem.id
                    imported_poems += 1

                except Exception as e:
                    errors.append(f"Poem #{idx + 1}: {str(e)}")

            if "comments.json" in zipf.namelist():
                try:
                    comments_data = json.loads(zipf.read("comments.json").decode("utf-8"))
                    for idx, cd in enumerate(comments_data.get("comments", [])):
                        try:
                            puuid = cd.get("poem_uuid")
                            if not puuid or puuid not in uuid_to_poem_id:
                                errors.append(f"Comment #{idx + 1}: poem not found")
                                continue
                            if "body" not in cd:
                                errors.append(f"Comment #{idx + 1}: missing body")
                                continue
                            db.add(Comment(
                                poem_id=uuid_to_poem_id[puuid],
                                author=cd.get("author", "Anonymous"),
                                body=cd["body"],
                                created_at=datetime.fromisoformat(cd["created_at"]) if cd.get("created_at") else datetime.utcnow(),
                            ))
                            imported_comments += 1
                        except Exception as e:
                            errors.append(f"Comment #{idx + 1}: {str(e)}")
                except Exception as e:
                    errors.append(f"Failed to import comments: {str(e)}")

            try:
                await db.commit()
            except Exception as e:
                await db.rollback()
                raise HTTPException(500, f"Failed to save data: {str(e)}")

            return {
                "imported_poems": imported_poems,
                "imported_comments": imported_comments,
                "errors": errors,
                "total_poems_attempted": len(poems_data["poems"])
            }

    except zipfile.BadZipFile:
        raise HTTPException(400, "Invalid zip archive")
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Import ERROR] {traceback.format_exc()}", file=sys.stderr)
        raise HTTPException(500, f"Import failed: {str(e)}")

# ====== PARAMETRIZED ROUTES ======
@router.get("/{poem_id}")
async def get_poem(poem_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Poem).options(selectinload(Poem.tags)).where(Poem.id == poem_id)
    )
    poem = result.scalar_one_or_none()
    if not poem:
        raise HTTPException(404, "Poem not found")
    return _poem_to_dict(poem)

@router.post("", status_code=201)
async def create_poem(data: PoemIn, admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    poem = Poem(title=data.title, body=data.body, is_draft=bool(data.is_draft))
    for tag_name in data.tags:
        tag_name = tag_name.strip().lower()
        if tag_name:
            poem.tags.append(await _get_or_create_tag(db, tag_name))
    db.add(poem)
    await db.commit()
    await db.refresh(poem)
    result = await db.execute(select(Poem).options(selectinload(Poem.tags)).where(Poem.id == poem.id))
    return _poem_to_dict(result.scalar_one())

@router.put("/{poem_id}")
async def update_poem(poem_id: int, data: PoemUpdate, admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Poem).options(selectinload(Poem.tags)).where(Poem.id == poem_id)
    )
    poem = result.scalar_one_or_none()
    if not poem:
        raise HTTPException(404, "Poem not found")

    last_v = await db.execute(
        select(PoemVersion).where(PoemVersion.poem_id == poem_id).order_by(desc(PoemVersion.version_number))
    )
    last_version = last_v.scalars().first()
    next_v = (last_version.version_number + 1) if last_version else 1

    db.add(PoemVersion(poem_id=poem_id, version_number=next_v,
                       title=poem.title, body=poem.body, image_filename=poem.image_filename))
    await db.flush()

    if data.title is not None:
        poem.title = data.title
    if data.body is not None:
        poem.body = data.body
    if data.is_draft is not None:
        poem.is_draft = bool(data.is_draft)

    if data.tags is not None:
        poem.tags.clear()
        for tag_name in data.tags:
            tag_name = tag_name.strip().lower()
            if tag_name:
                poem.tags.append(await _get_or_create_tag(db, tag_name))

    await db.commit()
    result = await db.execute(select(Poem).options(selectinload(Poem.tags)).where(Poem.id == poem_id))
    return _poem_to_dict(result.scalar_one())

@router.post("/{poem_id}/image")
async def upload_poem_image(poem_id: int, file: UploadFile = File(...), admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Poem).where(Poem.id == poem_id))
    poem = result.scalar_one_or_none()
    if not poem:
        raise HTTPException(404, "Poem not found")
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(400, "Invalid image type. Only JPG and PNG are allowed")
    content = await file.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(400, "Image is too large. Max size is 1MB")
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    ext = ALLOWED_IMAGE_TYPES[file.content_type]
    filename = f"{poem.uuid}{ext}"
    if poem.image_filename and poem.image_filename != filename:
        old_path = os.path.join(UPLOADS_DIR, poem.image_filename)
        if os.path.exists(old_path):
            os.remove(old_path)
    with open(os.path.join(UPLOADS_DIR, filename), "wb") as out:
        out.write(content)
    poem.image_filename = filename
    await db.commit()
    await db.refresh(poem)
    return {"ok": True, "image_url": _image_url(poem)}

@router.delete("/{poem_id}/image")
async def delete_poem_image(poem_id: int, admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Poem).where(Poem.id == poem_id))
    poem = result.scalar_one_or_none()
    if not poem:
        raise HTTPException(404, "Poem not found")
    if poem.image_filename:
        path = os.path.join(UPLOADS_DIR, poem.image_filename)
        if os.path.exists(path):
            os.remove(path)
        poem.image_filename = None
        await db.commit()
    return {"ok": True}

# ====== VERSIONS ======
@router.get("/{poem_id}/versions")
async def get_poem_versions(poem_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Poem).where(Poem.id == poem_id))
    poem = result.scalar_one_or_none()
    if not poem:
        raise HTTPException(404, "Poem not found")
    v_result = await db.execute(
        select(PoemVersion).where(PoemVersion.poem_id == poem_id).order_by(desc(PoemVersion.version_number))
    )
    versions = v_result.scalars().all()
    return {
        "poem_id": poem_id,
        "current_version": {
            "version_number": len(versions) + 1,
            "title": poem.title, "body": poem.body,
            "image_filename": poem.image_filename,
            "created_at": poem.updated_at.isoformat(), "is_current": True
        },
        "history": [
            {"version_number": v.version_number, "title": v.title, "body": v.body,
             "image_filename": v.image_filename, "created_at": v.created_at.isoformat(), "is_current": False}
            for v in versions
        ]
    }

@router.get("/{poem_id}/versions/{version_number}")
async def get_poem_version(poem_id: int, version_number: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Poem).where(Poem.id == poem_id))
    if not result.scalar_one_or_none():
        raise HTTPException(404, "Poem not found")
    v_result = await db.execute(
        select(PoemVersion).where(PoemVersion.poem_id == poem_id, PoemVersion.version_number == version_number)
    )
    version = v_result.scalar_one_or_none()
    if not version:
        raise HTTPException(404, "Version not found")
    return {
        "poem_id": poem_id, "version_number": version.version_number,
        "title": version.title, "body": version.body,
        "image_filename": version.image_filename, "created_at": version.created_at.isoformat()
    }

@router.post("/{poem_id}/restore/{version_number}")
async def restore_poem_version(poem_id: int, version_number: int, admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Poem).options(selectinload(Poem.tags)).where(Poem.id == poem_id))
    poem = result.scalar_one_or_none()
    if not poem:
        raise HTTPException(404, "Poem not found")
    v_result = await db.execute(
        select(PoemVersion).where(PoemVersion.poem_id == poem_id, PoemVersion.version_number == version_number)
    )
    version = v_result.scalar_one_or_none()
    if not version:
        raise HTTPException(404, "Version not found")

    last_v = await db.execute(
        select(PoemVersion).where(PoemVersion.poem_id == poem_id).order_by(desc(PoemVersion.version_number))
    )
    last_version = last_v.scalars().first()
    next_v = (last_version.version_number + 1) if last_version else 1

    db.add(PoemVersion(poem_id=poem_id, version_number=next_v,
                       title=poem.title, body=poem.body, image_filename=poem.image_filename))
    await db.flush()

    poem.title = version.title
    poem.body = version.body
    poem.image_filename = version.image_filename
    await db.commit()
    result = await db.execute(select(Poem).options(selectinload(Poem.tags)).where(Poem.id == poem_id))
    poem = result.scalar_one()
    return {"ok": True, "message": f"Restored to version {version_number}", "poem": _poem_to_dict(poem)}

@router.delete("/{poem_id}", status_code=204)
async def delete_poem(poem_id: int, admin: Admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Poem).where(Poem.id == poem_id))
    poem = result.scalar_one_or_none()
    if not poem:
        raise HTTPException(404, "Poem not found")
    if poem.image_filename:
        path = os.path.join(UPLOADS_DIR, poem.image_filename)
        if os.path.exists(path):
            os.remove(path)
    await db.delete(poem)
    await db.commit()
