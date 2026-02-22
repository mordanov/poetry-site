from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from database import get_db
from routers.auth import get_current_admin
from models import Poem, Tag, Comment, Admin
import io
import json
import os
import zipfile
import sys
import traceback
import base64

router = APIRouter()

UPLOADS_DIR = os.getenv("UPLOADS_DIR", "/app/data/uploads/poems")
MAX_IMAGE_SIZE = 1 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg": ".jpg", "image/png": ".png"}

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
    uuid: str
    title: str
    body: str
    image_url: Optional[str]
    created_at: str
    updated_at: str
    tags: List[str]

    class Config:
        from_attributes = True

def _image_url(poem: Poem) -> Optional[str]:
    if not poem.image_filename:
        return None
    return f"/uploads/poems/{poem.image_filename}"

def _poem_to_dict(poem: Poem) -> dict:
    return {
        "id": poem.id,
        "uuid": poem.uuid,
        "title": poem.title,
        "body": poem.body,
        "image_url": _image_url(poem),
        "created_at": poem.created_at.isoformat(),
        "updated_at": poem.updated_at.isoformat(),
        "tags": [t.name for t in poem.tags]
    }

# ====== LIST & FILTER ======
@router.get("")
def list_poems(
    tag: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all poems with pagination, optionally filtered by tag"""
    query = db.query(Poem).order_by(desc(Poem.created_at))
    if tag:
        query = query.join(Poem.tags).filter(Tag.name == tag.lower())

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    poems = query.offset(offset).limit(limit).all()

    return {
        "poems": [_poem_to_dict(poem) for poem in poems],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }

@router.get("/tags")
def list_tags(db: Session = Depends(get_db)):
    """Get all tags with poem counts"""
    tags = db.query(Tag).all()
    result = []
    for tag in tags:
        count = db.query(func.count(Poem.id)).join(Poem.tags).filter(Tag.id == tag.id).scalar()
        if count > 0:  # Only include tags with at least 1 poem
            result.append({"name": tag.name, "count": count})
    result.sort(key=lambda x: x["count"], reverse=True)
    return result

# ====== SPECIAL ROUTES (before {poem_id}) ======
@router.get("/uuid/{poem_uuid}")
def get_poem_by_uuid(poem_uuid: str, db: Session = Depends(get_db)):
    """Get a specific poem by UUID"""
    poem = db.query(Poem).filter(Poem.uuid == poem_uuid).first()
    if not poem:
        raise HTTPException(404, "Poem not found")
    return _poem_to_dict(poem)

@router.get("/export/poems")
def export_poems(admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Export poems, images, and comments into a zip archive (admin only)"""
    poems = db.query(Poem).order_by(Poem.uuid).all()

    poems_payload = []
    comments_payload = []

    for poem in poems:
        poems_payload.append({
            "uuid": poem.uuid,
            "title": poem.title,
            "body": poem.body,
            "tags": [t.name for t in poem.tags],
            "image_filename": poem.image_filename,
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
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(buffer, media_type="application/zip", headers=headers)

@router.post("/import")
async def import_poems(file: UploadFile = File(...), admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Import poems, images, and comments from a zip archive (admin only)"""
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

            print(f"[Import] Starting import of {len(poems_data['poems'])} poems", file=sys.stderr)

            for idx, poem_data in enumerate(poems_data["poems"]):
                try:
                    if "body" not in poem_data:
                        errors.append(f"Poem #{idx + 1}: missing 'body' field")
                        continue

                    poem_uuid = poem_data.get("uuid")
                    if not poem_uuid:
                        errors.append(f"Poem #{idx + 1}: missing 'uuid' field")
                        continue

                    existing_poem = db.query(Poem).filter(Poem.uuid == poem_uuid).first()
                    if existing_poem:
                        print(f"[Import] Poem {poem_uuid} already exists, skipping", file=sys.stderr)
                        errors.append(f"Poem #{idx + 1}: uuid already exists")
                        uuid_to_poem_id[poem_uuid] = existing_poem.id
                        continue

                    poem = Poem(
                        uuid=poem_uuid,
                        title=poem_data.get("title", ""),
                        body=poem_data["body"],
                        created_at=datetime.fromisoformat(poem_data.get("created_at")) if poem_data.get("created_at") else datetime.utcnow(),
                        updated_at=datetime.fromisoformat(poem_data.get("updated_at")) if poem_data.get("updated_at") else datetime.utcnow()
                    )

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

                    image_filename = poem_data.get("image_filename")
                    if image_filename:
                        image_entry = f"images/{image_filename}"
                        if image_entry in zipf.namelist():
                            try:
                                ext = os.path.splitext(image_filename)[1].lower()
                                if ext in (".jpg", ".jpeg", ".png"):
                                    target_filename = f"{poem.uuid}{'.png' if ext == '.png' else '.jpg'}"
                                    os.makedirs(UPLOADS_DIR, exist_ok=True)

                                    with zipf.open(image_entry) as img_file:
                                        image_bytes = img_file.read()

                                    if len(image_bytes) > MAX_IMAGE_SIZE:
                                        print(f"[Import] Image for poem {poem_uuid} too large, skipping", file=sys.stderr)
                                        errors.append(f"Poem #{idx + 1}: image too large")
                                    else:
                                        file_path = os.path.join(UPLOADS_DIR, target_filename)
                                        with open(file_path, "wb") as out:
                                            out.write(image_bytes)
                                        poem.image_filename = target_filename
                                        print(f"[Import] Imported image for poem {poem_uuid}: {target_filename}", file=sys.stderr)
                            except Exception as e:
                                print(f"[Import] Error importing image for poem {poem_uuid}: {str(e)}", file=sys.stderr)
                                errors.append(f"Poem #{idx + 1}: image import error: {str(e)}")

                    db.add(poem)
                    db.flush()
                    uuid_to_poem_id[poem_uuid] = poem.id
                    imported_poems += 1
                    print(f"[Import] Imported poem {poem_uuid}", file=sys.stderr)

                except Exception as e:
                    print(f"[Import] Error importing poem #{idx + 1}: {str(e)}", file=sys.stderr)
                    errors.append(f"Poem #{idx + 1}: {str(e)}")

            if "comments.json" in zipf.namelist():
                try:
                    comments_data = json.loads(zipf.read("comments.json").decode("utf-8"))
                    if "comments" in comments_data and isinstance(comments_data["comments"], list):
                        for idx, comment_data in enumerate(comments_data["comments"]):
                            try:
                                poem_uuid = comment_data.get("poem_uuid")
                                if not poem_uuid:
                                    errors.append(f"Comment #{idx + 1}: missing 'poem_uuid' field")
                                    continue

                                if poem_uuid not in uuid_to_poem_id:
                                    print(f"[Import] Poem {poem_uuid} not found for comment, skipping", file=sys.stderr)
                                    errors.append(f"Comment #{idx + 1}: poem with uuid {poem_uuid} not found")
                                    continue

                                if "body" not in comment_data:
                                    errors.append(f"Comment #{idx + 1}: missing 'body' field")
                                    continue

                                comment = Comment(
                                    poem_id=uuid_to_poem_id[poem_uuid],
                                    author=comment_data.get("author", "Anonymous"),
                                    body=comment_data["body"],
                                    created_at=datetime.fromisoformat(comment_data.get("created_at")) if comment_data.get("created_at") else datetime.utcnow()
                                )
                                db.add(comment)
                                imported_comments += 1

                            except Exception as e:
                                print(f"[Import] Error importing comment #{idx + 1}: {str(e)}", file=sys.stderr)
                                errors.append(f"Comment #{idx + 1}: {str(e)}")
                except Exception as e:
                    print(f"[Import] Error importing comments: {str(e)}", file=sys.stderr)
                    errors.append(f"Failed to import comments: {str(e)}")

            try:
                db.commit()
                print(f"[Import] Successfully imported {imported_poems} poems and {imported_comments} comments", file=sys.stderr)
            except Exception as e:
                db.rollback()
                print(f"[Import] Database commit error: {str(e)}", file=sys.stderr)
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
def get_poem(poem_id: int, db: Session = Depends(get_db)):
    """Get a specific poem"""
    poem = db.query(Poem).filter(Poem.id == poem_id).first()
    if not poem:
        raise HTTPException(404, "Poem not found")
    return _poem_to_dict(poem)

@router.post("", status_code=201)
def create_poem(data: PoemIn, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Create a new poem"""
    poem = Poem(title=data.title, body=data.body)

    for tag_name in data.tags:
        tag_name = tag_name.strip().lower()
        if tag_name:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()
            poem.tags.append(tag)

    db.add(poem)
    db.commit()
    db.refresh(poem)
    return _poem_to_dict(poem)

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
    return _poem_to_dict(poem)

@router.post("/{poem_id}/image")
async def upload_poem_image(poem_id: int, file: UploadFile = File(...), admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Upload or replace a poem image (admin only)"""
    poem = db.query(Poem).filter(Poem.id == poem_id).first()
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
    file_path = os.path.join(UPLOADS_DIR, filename)

    if poem.image_filename and poem.image_filename != filename:
        old_path = os.path.join(UPLOADS_DIR, poem.image_filename)
        if os.path.exists(old_path):
            os.remove(old_path)

    with open(file_path, "wb") as out:
        out.write(content)

    poem.image_filename = filename
    db.commit()
    db.refresh(poem)

    return {"ok": True, "image_url": _image_url(poem)}

@router.delete("/{poem_id}/image")
def delete_poem_image(poem_id: int, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Delete a poem image (admin only)"""
    poem = db.query(Poem).filter(Poem.id == poem_id).first()
    if not poem:
        raise HTTPException(404, "Poem not found")

    if poem.image_filename:
        image_path = os.path.join(UPLOADS_DIR, poem.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        poem.image_filename = None
        db.commit()

    return {"ok": True}

@router.post("/{poem_id}/generate-image")
async def generate_poem_image(poem_id: int, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Generate an image for a poem using GPT Image 1 (admin only)"""
    try:
        from openai import OpenAI
        from PIL import Image
        import requests
    except ImportError as e:
        raise HTTPException(500, f"Missing dependencies: {str(e)}. Install: pip install openai Pillow requests")

    try:
        poem = db.query(Poem).filter(Poem.id == poem_id).first()
        if not poem:
            raise HTTPException(404, "Poem not found")

        if poem.image_filename:
            raise HTTPException(400, "Poem already has an image. Delete it first if you want to generate a new one.")

        openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
        base_prompt = os.getenv("OPENAI_IMAGE_PROMPT", "Create an artistic illustration inspired by this poem.")

        if not openai_api_key:
            raise HTTPException(500, "OpenAI API key not configured. Set OPENAI_API_KEY in .env")

        if not openai_api_key.startswith("sk-"):
            raise HTTPException(500, "OpenAI API key format invalid. Should start with 'sk-'")

        prompt = f"{base_prompt}\n{poem.body[:500]}"

        print(f"[GPT-Image] Generating image for poem {poem.id} ({poem.uuid})", file=sys.stderr)
        print(f"[GPT-Image] Prompt: {prompt}...", file=sys.stderr)

        client = OpenAI(api_key=openai_api_key)

        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        if not response.data or len(response.data) == 0:
            raise HTTPException(500, "No image generated from OpenAI")

        image_data = response.data[0]
        image_url = None
        print(f"[GPT-Image] Response data: {image_data}", file=sys.stderr)

        if hasattr(image_data, 'url') and image_data.url:
            image_url = image_data.url
        elif hasattr(image_data, 'b64_json') and image_data.b64_json:
            image_bytes = base64.b64decode(image_data.b64_json)
            img = Image.open(io.BytesIO(image_bytes))
        else:
            print(f"[GPT-Image ERROR] Unexpected response format: {image_data}", file=sys.stderr)
            raise HTTPException(500, f"Unexpected response format from OpenAI API")

        if image_url:
            print(f"[GPT-Image] Generated image URL: {image_url[:50]}...", file=sys.stderr)
            img_response = requests.get(image_url, timeout=30)
            if img_response.status_code != 200:
                raise HTTPException(500, f"Failed to download generated image (status {img_response.status_code})")
            img = Image.open(io.BytesIO(img_response.content))

        print(f"[GPT-Image] Original image size: {img.width}x{img.height}", file=sys.stderr)

        compressed_size = (int(img.width * 0.5), int(img.height * 0.5))
        img = img.resize(compressed_size, Image.Resampling.LANCZOS)
        print(f"[GPT-Image] Compressed image size: {img.width}x{img.height}", file=sys.stderr)

        os.makedirs(UPLOADS_DIR, exist_ok=True)
        filename = f"{poem.uuid}.jpg"
        file_path = os.path.join(UPLOADS_DIR, filename)

        img.save(file_path, "JPEG", quality=75, optimize=True)
        print(f"[GPT-Image] Saved to: {file_path}", file=sys.stderr)

        poem.image_filename = filename
        db.commit()
        db.refresh(poem)

        return {
            "ok": True,
            "image_url": _image_url(poem),
            "message": f"Generated and compressed image for poem '{poem.title or 'untitled'}'"
        }

    except HTTPException:
        raise
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"[GPT-Image ERROR] {error_details}", file=sys.stderr)
        raise HTTPException(500, f"Failed to generate image: {str(e)}")

@router.delete("/{poem_id}", status_code=204)
def delete_poem(poem_id: int, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Delete a poem"""
    poem = db.query(Poem).filter(Poem.id == poem_id).first()
    if not poem:
        raise HTTPException(404, "Poem not found")

    if poem.image_filename:
        image_path = os.path.join(UPLOADS_DIR, poem.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.delete(poem)
    db.commit()

