import os
import shutil
import uuid
from typing import List
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import models, schemas, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Platform Web Novel & AU Chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "Backend Platform Novel & AU siap digunakan!"}

@app.post("/auth/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username atau email sudah terdaftar.")

    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=auth.hash_password(user.password),
        bio=user.bio
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Username atau password salah.")

    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload/image")
def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = f"static/uploads/{unique_name}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"url": f"/static/uploads/{unique_name}"}

@app.post("/stories", response_model=schemas.StoryResponse)
def create_story(
    story: schemas.StoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_story = models.Story(**story.model_dump(), author_id=current_user.id)
    db.add(new_story)
    db.commit()
    db.refresh(new_story)
    return new_story

@app.get("/stories", response_model=List[schemas.StoryResponse])
def get_all_stories(genre: str = None, search: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Story)
    if genre:
        query = query.filter(models.Story.genre.ilike(f"%{genre}%"))
    if search:
        query = query.filter(models.Story.title.ilike(f"%{search}%"))
    return query.all()

@app.get("/stories/{story_id}", response_model=schemas.StoryResponse)
def get_story_detail(story_id: int, db: Session = Depends(get_db)):
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Cerita tidak ditemukan.")
    return story

@app.post("/stories/{story_id}/characters", response_model=schemas.CharacterResponse)
def add_character(
    story_id: int,
    character: schemas.CharacterCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story or story.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Kamu tidak berhak mengubah cerita ini.")

    new_char = models.StoryCharacter(**character.model_dump(), story_id=story_id)
    db.add(new_char)
    db.commit()
    db.refresh(new_char)
    return new_char

@app.post("/stories/{story_id}/chapters", response_model=schemas.ChapterResponse)
def create_chapter(
    story_id: int,
    chapter: schemas.ChapterCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story or story.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Kamu tidak berhak menambah bab di cerita ini.")

    new_chapter = models.Chapter(**chapter.model_dump(), story_id=story_id)
    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)
    return new_chapter

@app.get("/stories/{story_id}/chapters", response_model=List[schemas.ChapterResponse])
def get_chapters_by_story(story_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Chapter)
        .filter(models.Chapter.story_id == story_id)
        .order_by(models.Chapter.chapter_number)
        .all()
    )

@app.get("/chapters/{chapter_id}", response_model=schemas.ChapterResponse)
def read_chapter(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Bab tidak ditemukan.")
    return chapter