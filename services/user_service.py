from datetime import datetime, timezone, timedelta
from typing import List, Optional

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
