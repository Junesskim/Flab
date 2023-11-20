from sqlmodel import Field, SQLModel
from typing import Optional

class Post(SQLModel, table=True):
    post_id: Optional[int] = Field(default=None, primary_key=True)
    author: str
    title: str
    content: str
    created_at: str
