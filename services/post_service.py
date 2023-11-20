from datetime import datetime, timezone, timedelta
from typing import List, Optional

from sqlmodel import Session

from domain.models import Post

seoul_timezone = timezone(timedelta(hours=9))

def create_post(session: Session, post: Post) -> None:
    current_time = datetime.now(tz=seoul_timezone)
    post.created_at = current_time.strftime("%Y-%m-%d %H:%M:%S")
    session.add(post)
    session.commit()
    session.refresh(post)

def get_all_posts(session: Session) -> List[Post]:
    posts = session.query(Post).all()
    return posts

def update_post(session: Session, post_id: int, updated_post: Post) -> Optional[Post]:
    existing_post = session.get(Post, post_id)
    if existing_post:
        for var, value in vars(updated_post).items():
            setattr(existing_post, var, value)
        session.commit()
        session.refresh(existing_post)
        return existing_post

def delete_post(session: Session, post_id: int) -> Optional[Post]:
    post = session.get(Post, post_id)
    if post:
        session.delete(post)
        session.commit()
        return post