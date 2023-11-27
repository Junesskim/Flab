from sqlmodel import Field, SQLModel
from typing import Optional

class Post(SQLModel, table=True):
    post_id: Optional[int] = Field(default=None, primary_key=True)
    author: str
    title: str
    content: str
    created_at: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str # 조건 : 길이 8자 이상, 하나 이상 대문자...
    nickname: str 
    created_at: str

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int
    post_id: int
    content: str
    created_at: str