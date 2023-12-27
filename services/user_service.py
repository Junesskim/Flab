from datetime import datetime, timezone, timedelta
from typing import List, Optional
import uuid

from sqlmodel import Session

from domain.models import User

seoul_timezone = timezone(timedelta(hours=9))

def create_user(session: Session, user: User) -> None:
    current_time = datetime.now(tz=seoul_timezone)
    user.created_at = current_time.strftime("%Y-%m-%d %H:%M:%S")
    session.add(user)
    session.commit()
    session.refresh(user)

def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def get_all_users(session: Session) -> List[User]:
    return session.query(User).all()

def create_token():
    return str(uuid.uuid4())

user_tokens_cache = {}

def find_token_by_user_id(user_id: str) -> Optional[str]:
    return user_tokens_cache.get(user_id)

def find_user_by_token(token: str, session: Session) -> Optional[User]:
    user_id = next(iter(user_tokens_cache.keys()))
    return session.get(User, user_id)

def delete_user_token(user_id: str) -> None:
    user_tokens_cache.pop(user_id, None)

def find_user_by_token(token: str, session: Session) -> Optional[User]:
    user_id = next(iter(user_tokens_cache.keys()))
    return session.get(User, user_id)