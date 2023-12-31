# FastAPI를 이용한 간단한 게시글 관리 REST API 서버

이 프로젝트는 FastAPI 라이브러리를 사용하여 REST API 서버를 구현한 것입니다. 
다음과 같은 기능을 제공합니다.

## 설치 사항
### 파이썬 설치
- Python >= 3.10
- fastapi/ sqlmodel 등 필요한 라이브러리는 poetry 참고

```curl
poetry install
```

## Docker
### Docker 실행
```curl
docker run -p 80:80 my-fastapi-app
```

## API 요구사항
### 1. 게시글 생성 (Create Post)
- POST 요청을 통해 새로운 게시글을 생성할 수 있습니다.
- 요청 본문에는 게시글 작성자, 제목, 내용을 포함해야 합니다.

  **Endpoint:** `POST /posts`
  ```
  curl -X POST "http://localhost:8000/api/posts/"
  ```
  
### 2. 게시글 조회 (Get Post)
- 특정 게시글을 조회할 수 있습니다.
- 게시글 아이디 (Id)를 이용하여 조회합니다.

  **Endpoint:** `GET /posts/{post_id}`
  ```
  curl -X GET "http://localhost:8000/api/posts/{post_id}"
  ```
  
### 3. 게시글 목록 조회 (List Posts)
- 모든 게시글을 조회할 수 있습니다.
- 게시글의 목록을 반환합니다.

  **Endpoint:** `GET /posts`
  ```
  curl -X GET "http://localhost:8000/api/posts/"
  ```
  
### 4. 게시글 수정 (Update Post)
- 게시글 작성자만 해당 게시글을 수정할 수 있습니다.
- 게시글 아이디 (Id)를 이용하여 수정할 수 있습니다.
- 요청 본문에는 수정할 제목과 내용이 포함되어야 합니다.

  **Endpoint:** `PUT /posts/{post_id}`
  ```
  curl -X PUT "http://localhost:8000/api/posts/{post_id}"
  ```

### 5. 게시글 patch
```
curl -X PATCH "http://localhost:8000/api/posts/{post_id}"
```

### 5. 게시글 삭제 (Delete Post)
- 게시글 작성자만 해당 게시글을 삭제할 수 있습니다.
- 게시글 아이디 (Id)를 이용하여 삭제할 수 있습니다.

  **Endpoint:** `DELETE /posts/{post_id}`
  ```
  curl -X DELETE "http://localhost:8000/api/posts/{post_id}"
  ```

### 6. 유저(User)
- 유저 아이디 (Id)
- 유저 비밀번호 (Password)
    - 길이는 최소 8자 이상이여야 합니다.
    - 대문자 1개 이상이 꼭 들어가야 합니다.
- 유저 닉네임 (Nickname)
- 유저 생성 날짜 (Created At)

  **Endpoint:** `GET /users/{user_id}`  
  ```
  curl -X POST "http://localhost:8000/api/users/"
  ```
### 7. 댓글(Comment)
- 댓글 아이디 (Id)
- 작성자 아이디 (Author Id)
    - 유저 아이디와 같습니다.
- 게시글 아이디 (Post Id)
    - 이 댓글이 작성된 게시글의 Id 입니다.
- 댓글 내용 (Content)
- 댓글 생성 날짜 (Created At)

  **Endpoint:** `GET /posts/{post_id}/comments/`    
  ```
  curl -X POST "http://localhost:8000/api/comments/"
  ```

## Architecture Diagram
  ```mermaid
  classDiagram
    API --|> Post_Service
    API --|> User_Service
    API --|> Comment_Service
    Post_Service --|> Domain
    User_Service --|> Domain
    Comment_Service --|> Domain
        class API{
        routes.py
        create_post_api()
        get_all_posts_api()
        get_post_api()
        patch_post_api()
        update_post_api()
        delete_post_api()
        create_user_api()
        get_user_by_id_api()
        get_all_users_api()
        create_comment_api()
        get_posts_by_user_id_api()
        get_posts_by_author_id_api()
        get_comments_by_id_api()
        get_comments_by_author_id_api()
        get_comments_by_post_id_api()
    }
    class Post_Service{
        post_service.py
        create_post()
        get_all_posts()
        get_post()
        patch_post()
        update_post()
        delete_post()
    }
    class User_Service{
        user_service.py
        create_user()
        get_user_by_id()
        get_all_users()
    }
    class Comment_Service{
        comment_service.py
        create_comment()
        get_comment_by_id()
        get_comments_by_author_id()
        get_comments_by_post_id()
    }
    class Domain{
        models.py
    }
  ```