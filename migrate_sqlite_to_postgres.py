#!/usr/bin/env python3
"""
One-shot migration script: SQLite → PostgreSQL for Poetry Site.

Usage:
    python migrate_sqlite_to_postgres.py \
        --sqlite /path/to/poetry.db \
        --postgres "postgresql://poetry_user:password@localhost:5432/poetry"

The script is idempotent: it skips rows that already exist (by uuid for poems,
by username for admin, by id=1 for about).
"""

import argparse
import sys
import uuid as uuid_lib
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ── helpers ──────────────────────────────────────────────────────────────────

def sqlite_engine(path: str):
    from sqlalchemy import event
    engine = create_engine(f"sqlite:///{path}", connect_args={"check_same_thread": False})
    @event.listens_for(engine, "connect")
    def set_pragmas(conn, _):
        conn.execute("PRAGMA foreign_keys=ON")
    return engine

def pg_engine(url: str):
    return create_engine(url, pool_pre_ping=True)

# ── migration ─────────────────────────────────────────────────────────────────

def migrate(sqlite_path: str, postgres_url: str, dry_run: bool = False) -> None:
    print(f"📂  Source SQLite : {sqlite_path}")
    print(f"🐘  Target Postgres: {postgres_url.split('@')[-1]}")  # hide credentials
    if dry_run:
        print("⚠️   DRY RUN — no data will be written\n")

    src = sessionmaker(bind=sqlite_engine(sqlite_path))()
    dst_engine = pg_engine(postgres_url)
    dst = sessionmaker(bind=dst_engine)()

    # Import models here so they are not required at module level
    # (allows running the script outside the Docker container with a venv)
    sys.path.insert(0, "backend")
    from models import Base, Admin, About, Poem, Tag, Comment, PoemVersion

    if not dry_run:
        print("🏗️   Creating schema on PostgreSQL...")
        Base.metadata.create_all(bind=dst_engine)

    # ── Admin ──────────────────────────────────────────────────────────────
    print("\n👤  Migrating admin...")
    admins = src.execute(text("SELECT id, username, password_hash FROM admin")).fetchall()
    admin_count = 0
    for row in admins:
        exists = dst.query(Admin).filter(Admin.username == row.username).first()
        if exists:
            print(f"   ↩  admin '{row.username}' already exists, skipping")
            continue
        if not dry_run:
            dst.add(Admin(username=row.username, password_hash=row.password_hash))
        admin_count += 1
        print(f"   ✅  admin '{row.username}'")
    if not dry_run:
        dst.commit()
    print(f"   → {admin_count} admin(s) migrated")

    # ── About ──────────────────────────────────────────────────────────────
    print("\n📖  Migrating about...")
    abouts = src.execute(text("SELECT id, name, bio, photo_url, updated_at FROM about")).fetchall()
    about_count = 0
    for row in abouts:
        exists = dst.query(About).filter(About.id == row.id).first()
        if exists:
            print(f"   ↩  about id={row.id} already exists, skipping")
            continue
        updated = datetime.fromisoformat(row.updated_at) if row.updated_at else datetime.utcnow()
        if not dry_run:
            dst.add(About(
                id=row.id,
                name=row.name,
                bio=row.bio or "",
                photo_url=row.photo_url,
                updated_at=updated,
            ))
        about_count += 1
        print(f"   ✅  about '{row.name}'")
    if not dry_run:
        dst.commit()
    print(f"   → {about_count} about record(s) migrated")

    # ── Tags ───────────────────────────────────────────────────────────────
    print("\n🏷️   Migrating tags...")
    tags_rows = src.execute(text("SELECT id, name FROM tags")).fetchall()
    sqlite_tag_id_to_dst: dict[int, Tag] = {}
    tag_count = 0
    for row in tags_rows:
        existing = dst.query(Tag).filter(Tag.name == row.name).first()
        if existing:
            sqlite_tag_id_to_dst[row.id] = existing
        else:
            tag = Tag(name=row.name)
            if not dry_run:
                dst.add(tag)
                dst.flush()
            sqlite_tag_id_to_dst[row.id] = tag
            tag_count += 1
    if not dry_run:
        dst.commit()
    print(f"   → {tag_count} new tag(s) migrated, {len(tags_rows) - tag_count} already existed")

    # ── Poems ──────────────────────────────────────────────────────────────
    print("\n📜  Migrating poems...")
    poems_rows = src.execute(text(
        "SELECT id, uuid, title, body, image_filename, generation_id, is_draft, "
        "created_at, updated_at FROM poems"
    )).fetchall()

    sqlite_poem_id_to_dst: dict[int, Poem] = {}
    poem_count = 0
    skipped_count = 0

    for row in poems_rows:
        poem_uuid = row.uuid or str(uuid_lib.uuid4())
        existing = dst.query(Poem).filter(Poem.uuid == poem_uuid).first()
        if existing:
            sqlite_poem_id_to_dst[row.id] = existing
            skipped_count += 1
            continue

        created = datetime.fromisoformat(row.created_at) if row.created_at else datetime.utcnow()
        updated = datetime.fromisoformat(row.updated_at) if row.updated_at else datetime.utcnow()

        poem = Poem(
            uuid=poem_uuid,
            title=row.title or "",
            body=row.body,
            image_filename=row.image_filename,
            generation_id=row.generation_id,
            is_draft=bool(row.is_draft),
            created_at=created,
            updated_at=updated,
        )

        # Attach tags via association table
        tag_links = src.execute(
            text("SELECT tag_id FROM poem_tags WHERE poem_id = :pid"),
            {"pid": row.id}
        ).fetchall()
        for (tag_id,) in tag_links:
            if tag_id in sqlite_tag_id_to_dst:
                poem.tags.append(sqlite_tag_id_to_dst[tag_id])

        if not dry_run:
            dst.add(poem)
            dst.flush()
        sqlite_poem_id_to_dst[row.id] = poem
        poem_count += 1

    if not dry_run:
        dst.commit()
    print(f"   → {poem_count} poem(s) migrated, {skipped_count} already existed")

    # ── Comments ───────────────────────────────────────────────────────────
    print("\n💬  Migrating comments...")
    comments_rows = src.execute(text(
        "SELECT id, poem_id, author, body, created_at FROM comments"
    )).fetchall()
    comment_count = 0
    for row in comments_rows:
        dst_poem = sqlite_poem_id_to_dst.get(row.poem_id)
        if not dst_poem or dst_poem.id is None:
            print(f"   ⚠️  comment id={row.id}: parent poem not found, skipping")
            continue
        created = datetime.fromisoformat(row.created_at) if row.created_at else datetime.utcnow()
        if not dry_run:
            dst.add(Comment(
                poem_id=dst_poem.id,
                author=row.author or "Anonymous",
                body=row.body,
                created_at=created,
            ))
        comment_count += 1
    if not dry_run:
        dst.commit()
    print(f"   → {comment_count} comment(s) migrated")

    # ── Poem versions ──────────────────────────────────────────────────────
    print("\n📋  Migrating poem versions...")
    has_versions = src.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name='poem_versions'")
    ).fetchone()
    version_count = 0
    if has_versions:
        versions_rows = src.execute(text(
            "SELECT id, poem_id, version_number, title, body, image_filename, created_at "
            "FROM poem_versions"
        )).fetchall()
        for row in versions_rows:
            dst_poem = sqlite_poem_id_to_dst.get(row.poem_id)
            if not dst_poem or dst_poem.id is None:
                continue
            created = datetime.fromisoformat(row.created_at) if row.created_at else datetime.utcnow()
            if not dry_run:
                dst.add(PoemVersion(
                    poem_id=dst_poem.id,
                    version_number=row.version_number,
                    title=row.title or "",
                    body=row.body,
                    image_filename=row.image_filename,
                    created_at=created,
                ))
            version_count += 1
        if not dry_run:
            dst.commit()
    print(f"   → {version_count} version(s) migrated")

    src.close()
    dst.close()

    print("\n✅  Migration complete!")
    print(f"   admins   : {admin_count}")
    print(f"   about    : {about_count}")
    print(f"   tags     : {tag_count}")
    print(f"   poems    : {poem_count}")
    print(f"   comments : {comment_count}")
    print(f"   versions : {version_count}")
    if dry_run:
        print("\n⚠️   DRY RUN — nothing was written to PostgreSQL")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate Poetry Site from SQLite to PostgreSQL")
    parser.add_argument("--sqlite",   required=True, help="Path to poetry.db SQLite file")
    parser.add_argument("--postgres", required=True, help="PostgreSQL connection URL")
    parser.add_argument("--dry-run",  action="store_true", help="Read SQLite but write nothing to Postgres")
    args = parser.parse_args()

    migrate(args.sqlite, args.postgres, dry_run=args.dry_run)

