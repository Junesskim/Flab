# FastAPI를 이용한 간단한 게시글 관리 REST API 서버

이 프로젝트는 FastAPI 라이브러리를 사용하여 REST API 서버를 구현한 것입니다. 
다음과 같은 기능을 제공합니다.

## 1. 게시글 생성 (Create Post)
- POST 요청을 통해 새로운 게시글을 생성할 수 있습니다.
- 요청 본문에는 게시글 작성자, 제목, 내용을 포함해야 합니다.

  **Endpoint:** `POST /posts`
  
## 2. 게시글 조회 (Get Post)
- 특정 게시글을 조회할 수 있습니다.
- 게시글 아이디 (Id)를 이용하여 조회합니다.

  **Endpoint:** `GET /posts/{post_id}`
  
## 3. 게시글 목록 조회 (List Posts)
- 모든 게시글을 조회할 수 있습니다.
- 게시글의 목록을 반환합니다.

  **Endpoint:** `GET /posts`
  
## 4. 게시글 수정 (Update Post)
- 게시글 작성자만 해당 게시글을 수정할 수 있습니다.
- 게시글 아이디 (Id)를 이용하여 수정할 수 있습니다.
- 요청 본문에는 수정할 제목과 내용이 포함되어야 합니다.

  **Endpoint:** `PUT /posts/{post_id}`

  
## 5. 게시글 삭제 (Delete Post)
- 게시글 작성자만 해당 게시글을 삭제할 수 있습니다.
- 게시글 아이디 (Id)를 이용하여 삭제할 수 있습니다.

  **Endpoint:** `DELETE /posts/{post_id}`

## 6. 유저(User)에는 다음 내용이 포함되어야 합니다.
- 유저 아이디 (Id)
- 유저 비밀번호 (Password)
    - 길이는 최소 8자 이상이여야 합니다.
    - 대문자 1개 이상이 꼭 들어가야 합니다.
- 유저 닉네임 (Nickname)
- 유저 생성 날짜 (Created At)

  **Endpoint:** `GET /users/{user_id}`  
## 7. 댓글(Comment)에는 다음 내용이 포함되어야 합니다.
- 댓글 아이디 (Id)
- 작성자 아이디 (Author Id)
    - 유저 아이디와 같습니다.
- 게시글 아이디 (Post Id)
    - 이 댓글이 작성된 게시글의 Id 입니다.
- 댓글 내용 (Content)
- 댓글 생성 날짜 (Created At)

  **Endpoint:** `GET /posts/{post_id}/comments/`    

  ```mermaid
  classDiagram
    API --|> Service
    Service --|> Domain
        class API{
        routes.py
        create_post_api()
        get_all_posts_api()
        get_post_api()
        patch_post_api()
        update_post_api()
        delete_post_api()
    }
    class Service{
        post_service.py
        create_post()
        get_all_posts()
        get_post()
        patch_post()
        update_post()
        delete_post()
    }
    class Domain{
        models.py
    }
  ```