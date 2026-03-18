"""
Webhook handlers for Leonardo.AI image generation completion
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import Poem
import io
import os
import sys
import traceback
import requests
from PIL import Image

router = APIRouter()

UPLOADS_DIR = os.getenv("UPLOADS_DIR", "/app/data/uploads/poems")
MAX_IMAGE_SIZE = 1 * 1024 * 1024


@router.post("/leonardo/image-generated")
async def leonardo_image_generated_webhook(payload: dict, db: AsyncSession = Depends(get_db)):
    """
    Webhook handler for Leonardo.AI image generation completion.
    Called by Leonardo.AI when image generation is complete.

    Expected payload:
    {
        "generationId": "...",
        "apiCreditCost": 1,
        "completedAt": "...",
        "images": [
            {
                "id": "...",
                "url": "https://...",
                "likeCount": 0,
                "nsfw": false,
                "generated": true
            }
        ],
        "status": "COMPLETE"
    }
    """
    try:
        generation_id = payload.get("generationId")
        status = payload.get("status")
        images = payload.get("images", [])

        print(f"[Leonardo Webhook] Received webhook for generation {generation_id} with status {status}", file=sys.stderr)

        if not generation_id:
            raise HTTPException(400, "Missing generationId in webhook payload")

        if status != "COMPLETE":
            print(f"[Leonardo Webhook] Generation {generation_id} not complete, status: {status}", file=sys.stderr)
            return {"ok": True, "message": f"Generation {generation_id} status: {status}"}

        if not images or len(images) == 0:
            print(f"[Leonardo Webhook ERROR] No images in webhook response for {generation_id}", file=sys.stderr)
            raise HTTPException(400, "No images in webhook payload")

        image_url = images[0].get("url")
        if not image_url:
            print(f"[Leonardo Webhook ERROR] No image URL in first image for {generation_id}", file=sys.stderr)
            raise HTTPException(400, "No image URL in webhook payload")

        result = await db.execute(select(Poem).where(Poem.generation_id == generation_id))
        poem = result.scalar_one_or_none()
        if not poem:
            print(f"[Leonardo Webhook ERROR] No poem found for generation {generation_id}", file=sys.stderr)
            raise HTTPException(404, f"Poem not found for generation {generation_id}")

        print(f"[Leonardo Webhook] Found poem {poem.id} ({poem.uuid}) for generation {generation_id}", file=sys.stderr)
        print(f"[Leonardo Webhook] Downloading image from {image_url[:50]}...", file=sys.stderr)

        # Download the image
        img_response = requests.get(image_url, timeout=30)
        if img_response.status_code != 200:
            print(f"[Leonardo Webhook ERROR] Failed to download image, status {img_response.status_code}", file=sys.stderr)
            raise HTTPException(500, f"Failed to download generated image (status {img_response.status_code})")

        image_bytes = img_response.content
        if len(image_bytes) > MAX_IMAGE_SIZE:
            print(f"[Leonardo Webhook ERROR] Image too large for {generation_id}", file=sys.stderr)
            raise HTTPException(400, "Generated image is too large")

        # Open image to verify and compress
        img = Image.open(io.BytesIO(image_bytes))
        print(f"[Leonardo Webhook] Original image size: {img.width}x{img.height}", file=sys.stderr)

        # Compress to 50%
        compressed_size = (int(img.width * 0.5), int(img.height * 0.5))
        img = img.resize(compressed_size, Image.Resampling.LANCZOS)
        print(f"[Leonardo Webhook] Compressed image size: {img.width}x{img.height}", file=sys.stderr)

        # Save image
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        filename = f"{poem.uuid}.jpg"
        file_path = os.path.join(UPLOADS_DIR, filename)

        img.save(file_path, "JPEG", quality=75, optimize=True)
        print(f"[Leonardo Webhook] Saved image to: {file_path}", file=sys.stderr)

        # Update poem with image
        poem.image_filename = filename
        poem.generation_id = None  # Clear generation_id after processing
        await db.commit()
        await db.refresh(poem)

        print(f"[Leonardo Webhook] Successfully saved image for poem {poem.id}", file=sys.stderr)

        return {
            "ok": True,
            "message": f"Image for generation {generation_id} saved successfully",
            "poem_id": poem.id,
            "image_url": f"/uploads/poems/{filename}"
        }

    except HTTPException:
        raise
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"[Leonardo Webhook ERROR] {error_details}", file=sys.stderr)
        raise HTTPException(500, f"Webhook processing failed: {str(e)}")

