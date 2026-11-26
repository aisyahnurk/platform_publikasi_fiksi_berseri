from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Optional, Literal
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    bio: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    bio: Optional[str] = None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CharacterCreate(BaseModel):
    name: str
    avatar_url: Optional[str] = None
    position: Literal["left", "right"] = "left"
    bubble_color: str = "#E5E7EB"

class CharacterResponse(CharacterCreate):
    id: int
    story_id: int
    class Config:
        from_attributes = True

class ChatBubble(BaseModel):
    character_id: Optional[int] = None
    type: Literal["text", "image", "narration"] = "text"
    text: Optional[str] = None
    image_url: Optional[str] = None
    time: Optional[str] = None

class ChapterCreate(BaseModel):
    chapter_number: int
    title: str
    format_type: Literal["narrative", "chat"]
    narrative_content: Optional[str] = None
    chat_content: Optional[List[ChatBubble]] = None
    is_published: bool = True

    @model_validator(mode="after")
    def validate_mode_content(self):
        if self.format_type == "narrative" and not self.narrative_content:
            raise ValueError("narrative_content wajib diisi jika memilih mode Wattpad (narrative).")
        if self.format_type == "chat" and not self.chat_content:
            raise ValueError("chat_content wajib diisi jika memilih mode AU (chat).")
        return self

class ChapterResponse(BaseModel):
    id: int
    story_id: int
    chapter_number: int
    title: str
    format_type: str
    narrative_content: Optional[str] = None
    chat_content: Optional[List[dict]] = None
    is_published: bool
    created_at: datetime
    class Config:
        from_attributes = True

class StoryCreate(BaseModel):
    title: str
    synopsis: Optional[str] = None
    genre: str
    cover_url: Optional[str] = None

class StoryResponse(StoryCreate):
    id: int
    author_id: int
    status: str
    created_at: datetime
    characters: List[CharacterResponse] = []
    class Config:
        from_attributes = True