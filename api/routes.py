from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from domain.models import Post
from services.post_service import create_post, get_all_posts, get_post, update_post, patch_post, delete_post

router = APIRouter()

@router.post("/posts/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post_api(post: Post, session: Session = Depends(get_session)):
    create_post(session, post)
    return post

@router.get("/posts/", response_model=List[Post], status_code=status.HTTP_200_OK)
def get_all_posts_api(session: Session = Depends(get_session)):
    return get_all_posts(session)

@router.get("/posts/", response_model=Post, status_code=status.HTTP_200_OK)
def get_all_posts_api(session: Session = Depends(get_session)):
    return get_post(session)

@router.put("/posts/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
def update_post_api(post_id: int, updated_post: Post, session: Session = Depends(get_session)):
    post = update_post(session, post_id, updated_post)
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post

@router.patch("/posts/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
def patch_post_api(post_id: int, updated_fields: dict, session: Session = Depends(get_session)):
    post = patch_post(session, post_id, updated_fields)
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

@router.delete("/posts/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
def delete_post_api(post_id: int, session: Session = Depends(get_session)):
    post = delete_post(session, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post
