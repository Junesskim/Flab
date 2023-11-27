from fastapi import FastAPI

from api.routes import router as api_router

app = FastAPI()

# API 라우터를 등록합니다.
app.include_router(api_router, prefix="/api")

# FastAPI 애플리케이션을 실행하기 위한 코드입니다.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
