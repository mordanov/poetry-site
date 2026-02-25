"""
SQLAlchemy ORM Models for Poetry Site
Defines all database tables using SQLAlchemy declarative base
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, func, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

# Association table for many-to-many relationship between poems and tags
poem_tags = Table(
    'poem_tags',
    Base.metadata,
    Column('poem_id', Integer, ForeignKey('poems.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


class Admin(Base):
    """Administrator account model"""
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Admin(username='{self.username}')>"


class About(Base):
    """About page content model"""
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True, default=1)
    name = Column(String(255), nullable=False, default='Lev Gorev')
    bio = Column(Text, nullable=False, default='')
    photo_url = Column(String(500), nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<About(name='{self.name}')>"


class Poem(Base):
    """Poem model with relationships to tags and comments"""
    __tablename__ = "poems"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, nullable=False, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False, default='')
    body = Column(Text, nullable=False)
    image_filename = Column(String(255), nullable=True)
    generation_id = Column(String(255), nullable=True, unique=True, index=True)
    is_draft = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    tags = relationship(
        "Tag",
        secondary=poem_tags,
        back_populates="poems",
        cascade="all"
    )
    comments = relationship(
        "Comment",
        back_populates="poem",
        cascade="all, delete-orphan"
    )
    versions = relationship(
        "PoemVersion",
        back_populates="poem",
        cascade="all, delete-orphan",
        order_by="PoemVersion.version_number.desc()"
    )

    def __repr__(self):
        return f"<Poem(title='{self.title[:50]}...')>"


class Tag(Base):
    """Tag model for categorizing poems"""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)

    # Relationships
    poems = relationship(
        "Poem",
        secondary=poem_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag(name='{self.name}')>"


class Comment(Base):
    """Comment/reflection model on poems"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    poem_id = Column(Integer, ForeignKey('poems.id', ondelete='CASCADE'), nullable=False, index=True)
    author = Column(String(255), nullable=False, default='Anonymous')
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)

    # Relationships
    poem = relationship("Poem", back_populates="comments")

    def __repr__(self):
        return f"<Comment(author='{self.author}', poem_id={self.poem_id})>"


class PoemVersion(Base):
    """Poem version history model - tracks all edits"""
    __tablename__ = "poem_versions"

    id = Column(Integer, primary_key=True, index=True)
    poem_id = Column(Integer, ForeignKey('poems.id', ondelete='CASCADE'), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)  # Sequential version number
    title = Column(String(500), nullable=False, default='')
    body = Column(Text, nullable=False)
    image_filename = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)

    # Relationships
    poem = relationship("Poem", back_populates="versions")

    __table_args__ = (
        UniqueConstraint('poem_id', 'version_number', name='uq_poem_version'),
    )

    def __repr__(self):
        return f"<PoemVersion(poem_id={self.poem_id}, version={self.version_number})>"
