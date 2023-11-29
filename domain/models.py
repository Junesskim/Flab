from sqlmodel import Field, SQLModel
import pytz
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

    def __init__(self, password: str, nickname: str):
        if len(password) <8 and password.islower() == password:
            raise ValueError("대문자 1개 이상 포함이고 길이는 최소 8자 이상이여야 합니다.")
        self.password = password
        self.nickname = nickname
        self.created_at = pytz.timezone('Asia/Seoul')

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int
    post_id: int
    content: str
    created_at: str