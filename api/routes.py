import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, SQLModel

from domain.models import Post, User, Comment
from services.post_service import create_post, get_all_posts, get_post, update_post, patch_post, delete_post, get_post_by_id, get_posts_by_author_id
from services.user_service import create_user, get_user_by_id, get_all_users
from services.comment_service import create_comment, get_comment_by_id, get_comments_by_author_id, get_comments_by_post_id

router = APIRouter()

class CreatePostRequest(SQLModel):
    title : str
    decription : str
    author_id : str
    request_at : datetime

class CreatePostResponse(SQLModel):
    id: str
    title: str
    content: str
    author_id: str
    created_at : datetime

@router.post("/posts/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post_api(request: CreatePostRequest, session: Session = Depends(get_session)) -> CreatePostResponse:
    post = create_post(session, request)
    
    return CreatePostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        created_at=post.created_at
    )

class GetAllPostsResponse(SQLModel):
    data : list[Post]

@router.get("/posts/", response_model=List[Post], status_code=status.HTTP_200_OK)
def get_all_posts_api(session: Session = Depends(get_session)) -> GetAllPostsResponse:
    posts = get_all_posts(session)
    return GetAllPostsResponse(
        data= posts
    )

class GetPostResponse(SQLModel):
    data : Post

@router.get("/posts/", response_model=Post, status_code=status.HTTP_200_OK)
def get_post(session: Session = Depends(get_session)) -> GetPostResponse:
    post = get_post(session)
    return GetPostResponse(
        data=post
    )


@router.put("/posts/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
def update_post_api(post_id: int, updated_post: Post, session: Session = Depends(get_session)):
    post = update_post(session, post_id, updated_post)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")
    return post

@router.patch("/posts/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
def patch_post_api(post_id: int, updated_fields: dict, session: Session = Depends(get_session)):
    post = patch_post(session, post_id, updated_fields)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")
    return post

@router.delete("/posts/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
def delete_post_api(post_id: int, session: Session = Depends(get_session)):
    post = delete_post(session, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")
    return post

@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_api(user: User, session: Session = Depends(get_session)):
    create_user(session, user)
    return user

@router.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def get_user_by_id_api(user_id: int, session: Session = Depends(get_session)):
    user = get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")
    return user

@router.get("/users/", response_model=List[User], status_code=status.HTTP_200_OK)
def get_all_users_api(session: Session = Depends(get_session)):
    return get_all_users(session)

@router.post("/comments/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment_api(comment: Comment, session: Session = Depends(Get_session)):
    create_comment(session, comment)
    return comment

@router.get("/users/{user_id}/posts/", response_model=List[Post], status_code=status.HTTP_200_OK)
def get_posts_by_user_id_api(user_id: int, session: Session = Depends(get_session)):
    return get_post_by_id(session, user_id)

@router.get("/users/{author_id}/posts/", response_model=List[Post], status_code=status.HTTP_200_OK)
def get_posts_by_author_id_api(user_id: int, session: Session = Depends(get_session)):
    return get_posts_by_author_id(session, user_id)

@router.get("/users/{id}/comments/", response_model=List[Comment], status_code=status.HTTP_200_OK)
def get_comments_by_id_api(user_id: int, session: Session = Depends(get_session)):
    return get_comment_by_id(session, user_id)

@router.get("/users/{author_id}/comments/", response_model=List[Comment], status_code=status.HTTP_200_OK)
def get_comments_by_author_id_api(user_id: int, session: Session = Depends(get_session)):
    return get_comments_by_author_id(session, user_id)

@router.get("/posts/{post_id}/comments/", response_model=List[Comment], status_code=status.HTTP_200_OK)
def get_comments_by_post_id_api(post_id: int, session: Session = Depends(get_session)):
    return get_comments_by_post_id(session, post_id)
