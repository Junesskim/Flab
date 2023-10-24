from datetime import datetime
from typing import Dict, List
import pytz

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import SQLModel, create_engine, Session, Field
from databases import Database

app = FastAPI()

# 게시글을 저장할 인메모리 데이터베이스
post_data = []
post_id_counter = 1

seoul_timezone = pytz.timezone("Asia/Seoul") 

Database_URL = "sqlite:///./API_Test.db"

database = Database(Database_URL)
metadata = SQLModel.metadata
engine = create_engine(Database_URL)
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

def create_post(post: Post):
    global post_id_counter  
    current_time = datetime.now(seoul_timezone)
    post_id = post_id_counter
    
    post_data.append({
        "post_id": post_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "created_at": current_time.strftime("%Y-%m-%d %H:%M:%S")
    })
    
    post_id_counter += 1
    return post_data[-1]

def get_all_posts():
    return post_data

def update_post(post_id: int, author: str, title: str, content: str):
    for post in post_data:
        if post["post_id"] == post_id:
            post["author"] = author
            post["title"] = title
            post["content"] = content
            return post
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

def delete_post(post_id: int):
    for index, post in enumerate(post_data):
        if post["post_id"] == post_id:
            deleted_post = post_data.pop(index)
            return deleted_post
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

@app.post("/posts/", response_model=Post, status_code=201)
def create_post_endpoint(post_id: int, author: str, title: str, content: str, session: Session = Depends(get_session)):
    session.add(post_id)
    session.commit()
    session.refresh(post_id)
    return create_post(post_id)

@app.get("/posts/", response_model=List[Post], status_code=201)
def get_all_post_endpoint(post_id: int, author: str, title: str, content: str):
    return get_all_posts(post_id)

@app.put("/posts/{post_id}", status_code=201)
def update_post_endpoint(post_id: int, author: str, title: str, content: str):
    return update_post(post_id, author, title, content)

@app.delete("/posts/{post_id}", status_code=201)
def delete_post_endpoint(post_id: int):
    return delete_post(post_id)
