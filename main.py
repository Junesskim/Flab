from datetime import datetime, timezone, timedelta
from typing import Dict, List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine

app = FastAPI()

seoul_timezone = timezone(timedelta(hours=9))

database_url = "sqlite:///./API_Test.db"

metadata = SQLModel.metadata
engine = create_engine(database_url)
metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

class Post(SQLModel, table=True):
    post_id: int = Field(default=None, primary_key=True)
    author: str
    title: str
    content: str
    created_at: str

def create_post(post: Post, session: Session = Depends(Session)):
    current_time = datetime.now(tz=seoul_timezone)
    post.created_at = current_time.strftime("%Y-%m-%d %H:%M:%S")
    session.add(post)
    session.commit()
    session.refresh(post)
    

def get_all_posts(session: Session = Depends(Session)) -> list[Post]:
    posts = session.query(Post).all()
    return posts

def update_post(post_id: int, post: Post, session: Session = Depends(Session)) -> Post:
    existing_post = session.get(Post, post_id)
    if existing_post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    for var, value in vars(post).items():
        setattr(existing_post, var, value)
    session.commit()
    session.refresh(existing_post)
    return existing_post

def delete_post(post_id: int, session: Session = Depends(Session)) -> Post:
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    session.delete(post)
    session.commit()
    return post

@app.post("/posts/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    return create_post(post)

@app.get("/posts/", response_model=List[Post], status_code=status.HTTP_200_OK)
def get_all_post():
    return get_all_posts()

@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, post: Post):
    return update_post(post_id, post)

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: int):
    return delete_post(post_id)
