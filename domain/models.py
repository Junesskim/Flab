from sqlmodel import Field, SQLModel
from pydantic import constr, validator
from typing import Optional


class Post(SQLModel, table=True):
    post_id: Optional[int] = Field(default=None, primary_key=True)
    author: str
    title: str
    content: str
    created_at: str


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: constr(min_length=8)  # 조건 : 길이 8자 이상, 하나 이상 대문자...
    nickname: str
    created_at: str

    @validator("password")
    def validator_password(cls, value):
        if not any(char.isupper() for char in value):
            raise ValueError("대문자 1개 이상 포함이고 길이는 최소 8자 이상이여야 합니다.")
        return value


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int
    post_id: int
    content: str
    created_at: str
