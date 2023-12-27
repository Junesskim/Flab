from datetime import datetime, timezone, timedelta
from typing import List, Optional

from sqlmodel import Session

from domain.models import Comment

seoul_timezone = timezone(timedelta(hours=9))


def create_comment(session: Session, comment: Comment) -> None:
    current_time = datetime.now(tz=seoul_timezone)
    comment.created_at = current_time.strftime("%Y-%m-%d %H:%M:%S")
    session.add(comment)
    session.commit()
    session.refresh(comment)


def get_comment_by_id(session: Session, comment_id: int) -> Optional[Comment]:
    return session.get(Comment, comment_id)


def get_comments_by_author_id(session: Session, author_id: int) -> List[Comment]:
    return session.query(Comment).filter(Comment.author_id == author_id).all()


def get_comments_by_post_id(session: Session, post_id: int) -> List[Comment]:
    return session.query(Comment).filter(Comment.post_id == post_id).all()
