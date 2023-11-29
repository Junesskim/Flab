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
