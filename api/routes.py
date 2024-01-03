from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlmodel import Session
from pydantic import BaseModel

from domain.models import Post, User, Comment
from services.post_service import (
    create_post,
    get_all_posts,
    get_post,
    update_post,
    patch_post,
    delete_post,
    get_post_by_id,
    get_posts_by_author_id,
)
from services.user_service import (
    create_user,
    get_user_by_id,
    get_all_users,
    create_token,
    find_token_by_user_id,
    find_user_by_token,
    delete_user_token,
)
from services.comment_service import (
    create_comment,
    get_comment_by_id,
    get_comments_by_author_id,
    get_comments_by_post_id,
)

router = APIRouter()

# 데이터베이스 연결 설정
DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)

# ENGINES 변수 설정
ENGINES = engine

# SQLModel의 Session 클래스를 사용하도록 수정
def get_session() -> SQLAlchemySession:
    with Session(ENGINES) as session:
        return session

class CreatePostRequest(BaseModel):
    token: str
    title: str
    description: str
    author_id: str
    request_at: datetime


class CreatePostResponse(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    created_at: datetime


@router.post(
    "/posts/", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED
)
def create_post_api(
    request: CreatePostRequest, session: Session = Depends(get_session)
) -> CreatePostResponse:
    token = request.token
    user = find_user_by_token(token, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="인증되지 않은 사용자 입니다!"
        )
    post = create_post(session, request)

    return CreatePostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        created_at=post.created_at,
    )


class GetAllPostsResponse(BaseModel):
    data: list[Post]


@router.get(
    "/posts/", response_model=GetAllPostsResponse, status_code=status.HTTP_200_OK
)
def get_all_posts_api(session: Session = Depends(get_session)) -> GetAllPostsResponse:
    posts = get_all_posts(session)
    return GetAllPostsResponse(data=posts)


class GetPostResponse(BaseModel):
    data: Post


@router.get("/posts/", response_model=GetPostResponse, status_code=status.HTTP_200_OK)
def get_post(session: Session = Depends(get_session)) -> GetPostResponse:
    post = get_post(session)
    return GetPostResponse(data=post)


class UpdatedPostRequest(BaseModel):
    token: str
    title: Optional[str] = None
    content: Optional[str] = None


class UpdatePostResponse(BaseModel):
    post_id: str
    author: str
    title: str
    content: str
    created_at: str


@router.put(
    "/posts/{post_id}",
    response_model=UpdatePostResponse,
    status_code=status.HTTP_200_OK,
)
def update_post_api(
    post_id: int,
    updated_post: UpdatedPostRequest,
    session: Session = Depends(get_session),
) -> UpdatePostResponse:
    post = session.get(Post, post_id)
    token = UpdatedPostRequest.token
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다."
        )

    user = find_user_by_token(token, session)
    if user.id != post.author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="본인의 게시글만 수정할 수 있습니다."
        )

    fields = updated_post.dict()
    post = update_post(session, post_id, fields)
    return UpdatePostResponse(
        post_id=post.post_id,
        author=post.author,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
    )


class PatchPostRequest(BaseModel):
    token: str
    title: Optional[str] = None
    content: Optional[str] = None


class PatchPostResponse(BaseModel):
    post_id: str
    author: str
    title: str
    content: str
    created_at: str


@router.patch(
    "/posts/{post_id}", response_model=PatchPostResponse, status_code=status.HTTP_200_OK
)
def patch_post_api(
    post_id: int,
    updated_fields: PatchPostRequest,
    session: Session = Depends(get_session),
) -> PatchPostResponse:
    post = session.get(Post, post_id)
    token = UpdatedPostRequest.token

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다."
        )

    user = find_user_by_token(token, session)
    if user.id != post.author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="본인의 게시글만 수정할 수 있습니다."
        )

    fields = updated_fields.dict(exclude_unset=True)
    post = patch_post(session, post_id, fields)
    return PatchPostResponse(
        post_id=post.post_id,
        author=post.author,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
    )


class DeletePostResponse(BaseModel):
    token: str
    post_id: str
    author: str
    title: str
    content: str
    created_at: str


@router.delete(
    "/posts/{post_id}",
    response_model=DeletePostResponse,
    status_code=status.HTTP_200_OK,
)
def delete_post_api(
    post_id: int, session: Session = Depends(get_session)
) -> DeletePostResponse:
    post = session.get(Post, post_id)
    token = UpdatedPostRequest.token

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다."
        )

    user = find_user_by_token(token, session)
    if user.id != post.author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="본인의 게시글만 수정할 수 있습니다."
        )

    post = delete_post(session, post_id)
    return DeletePostResponse(
        post_id=post.post_id,
        author=post.author,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
    )


class UserResponse(BaseModel):
    id: int
    nickname: str
    created_at: str


@router.post(
    "/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user_api(
    user: User, session: Session = Depends(get_session)
) -> UserResponse:
    create_user(session, user)

    return UserResponse(id=user.id, nickname=user.nickname, created_at=user.created_at)


get_user_by_id_cache = {}


@router.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def get_user_by_id_api(user_id: int, session: Session = Depends(get_session)):
    if user_id in get_user_by_id_cache:
        return get_user_by_id_cache[user_id]
    else:
        user = get_user_by_id(session, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다."
            )
        get_user_by_id_cache[user_id] = user
    return user


class GetAllUsersResponse(BaseModel):
    id: int
    password: str
    nickname: str
    created_at: str


@router.get(
    "/users/", response_model=List[GetAllUsersResponse], status_code=status.HTTP_200_OK
)
def get_all_users_api(session: Session = Depends(get_session)) -> GetAllUsersResponse:
    users = get_all_users(session)

    return GetAllUsersResponse(
        id=users.id,
        password=users.password,
        nickname=users.nickname,
        created_at=users.created_at,
    )


class CreateCommentRequest(BaseModel):
    author_id: int
    post_id: int
    content: str


class CreateCommentResponse(BaseModel):
    comment_id: int
    author_id: int
    post_id: int
    content: str
    created_at: str


@router.post(
    "/comments/",
    response_model=CreateCommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment_api(
    comment: CreateCommentRequest, session: Session = Depends(get_session)
) -> CreateCommentResponse:
    new_comment = Comment(
        author_id=comment.author_id, post_id=comment.post_id, content=comment.content
    )

    create_comment(session, new_comment)

    return CreateCommentResponse(
        comment_id=new_comment.id,
        author_id=new_comment.author_id,
        post_id=new_comment.post_id,
        content=new_comment.content,
        created_at=new_comment.created_at,
    )


get_posts_by_user_id_cache = {}


@router.get(
    "/users/{user_id}/posts/", response_model=List[Post], status_code=status.HTTP_200_OK
)
def get_posts_by_user_id_api(user_id: int, session: Session = Depends(get_session)):
    if user_id in get_posts_by_user_id_cache:
        return get_posts_by_user_id_cache[user_id]
    else:
        user = get_posts_by_user_id_api(session, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다."
            )
        get_posts_by_user_id_cache[user_id] = user
    return user


get_posts_by_author_id_cache = {}


@router.get(
    "/users/{author_id}/posts/",
    response_model=List[Post],
    status_code=status.HTTP_200_OK,
)
def get_posts_by_author_id_api(author_id: int, session: Session = Depends(get_session)):
    if author_id in get_posts_by_author_id_cache:
        return get_posts_by_author_id_cache[author_id]
    else:
        author = get_posts_by_author_id_api(session, author_id)
        if author is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다."
            )
        get_posts_by_author_id_cache[author_id] = author
    return author


get_comments_by_id_cache = {}


@router.get(
    "/users/{id}/comments/",
    response_model=List[Comment],
    status_code=status.HTTP_200_OK,
)
def get_comments_by_id_api(user_id: int, session: Session = Depends(get_session)):
    if user_id in get_comments_by_id_cache:
        return get_comments_by_id_cache[user_id]
    else:
        user = get_comments_by_id_api(session, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다."
            )
        get_comments_by_id_cache[user_id] = user
    return user


get_comments_by_author_id_cache = {}


@router.get(
    "/users/{author_id}/comments/",
    response_model=List[Comment],
    status_code=status.HTTP_200_OK,
)
def get_comments_by_author_id_api(
    author_id: int, session: Session = Depends(get_session)
):
    if author_id in get_comments_by_author_id_cache:
        return get_comments_by_author_id_cache[author_id]
    else:
        author = get_comments_by_author_id_api(session, author_id)
        if author is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다."
            )
        get_comments_by_author_id_cache[author_id] = author
    return author


get_comments_by_post_id_cache = {}


@router.get(
    "/posts/{post_id}/comments/",
    response_model=List[Comment],
    status_code=status.HTTP_200_OK,
)
def get_comments_by_post_id_api(post_id: int, session: Session = Depends(get_session)):
    if post_id in get_comments_by_post_id_cache:
        return get_comments_by_post_id_cache[post_id]
    else:
        post = get_comments_by_post_id_api(session, post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다."
            )
        get_comments_by_post_id_cache[post_id] = post
    return post


class LoginRequest(BaseModel):
    id: str
    password: str


class LoginResponse(BaseModel):
    token: str


user_tokens_cache = {}


@router.post(
    "/users/login", response_model=LoginResponse, status_code=status.HTTP_200_OK
)
def login(
    request: LoginRequest, session: Session = Depends(get_session)
) -> LoginResponse:
    user = session.get(User, request.id)
    if (user is None) or (user.password != request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="인증 실패입니다!"
        )

    delete_user_token(request.id)

    token = create_token()
    user_tokens_cache[request.id] = token

    return LoginResponse(token=token)
