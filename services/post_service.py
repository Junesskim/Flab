from datetime import datetime
import pytz
from typing import List, Optional

from sqlmodel import Session

from domain.models import Post

# seoul_timezone = timezone(timedelta(hours=9))
seoul_timezone = pytz.timezone('Asia/Seoul')

def create_post(session: Session, post: Post) -> None:
    current_time = datetime.now(tz=seoul_timezone)
    post.created_at = current_time.strftime("%Y-%m-%d %H:%M:%S")
    session.add(post)
    session.commit()
    session.refresh(post)

def get_all_posts(session: Session) -> List[Post]:
    posts = session.query(Post).all()
    return posts

def get_post(session: Session) -> Optional[Post]:
    post = session.query(Post)
    return post

def update_post(session: Session, post_id: int, updated_post: Post) -> Optional[Post]:
    existing_post = session.get(Post, post_id)
    if existing_post:
        for var, value in vars(updated_post).items():
            setattr(existing_post, var, value)
        session.commit()
        session.refresh(existing_post)
        return existing_post
    
def patch_post(session: Session, post_id: int, updated_fields: dict) -> Optional[Post]:
    existing_post = session.get(Post, post_id)
    if existing_post:
        for field, value in updated_fields.items():
            setattr(existing_post, field, value)
        session.commit()
        session.refresh(existing_post)
        return existing_post

def delete_post(session: Session, post_id: int) -> Optional[Post]:
    post = session.get(Post, post_id)
    if post:
        session.delete(post)
        session.commit()
        return post

def get_post_by_id(session: Session, post_id: int) -> Optional[Post]:
    return session.get(Post, post_id)

def get_posts_by_author_id(session: Session, author_id: int) -> List[Post]:
    return session.query(Post).filter(Post.author_id == author_id).all()
