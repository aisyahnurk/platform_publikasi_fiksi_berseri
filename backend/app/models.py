from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    stories = relationship("Story", back_populates="author")


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    synopsis = Column(Text, nullable=True)
    genre = Column(String(50), nullable=False)
    cover_url = Column(String(255), nullable=True)
    status = Column(String(20), default="ongoing")
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="stories")
    characters = relationship("StoryCharacter", back_populates="story", cascade="all, delete")
    chapters = relationship("Chapter", back_populates="story", cascade="all, delete")


class StoryCharacter(Base):
    __tablename__ = "story_characters"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    position = Column(String(10), default="left")
    bubble_color = Column(String(20), default="#E5E7EB")

    story = relationship("Story", back_populates="characters")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    format_type = Column(String(20), nullable=False)  # "narrative" atau "chat"
    narrative_content = Column(Text, nullable=True)
    chat_content = Column(JSON, nullable=True)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    story = relationship("Story", back_populates="chapters")