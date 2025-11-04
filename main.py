from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from modules.auth.routers import router as auth_router
from modules.posts.routers import router as post_router
from modules.comment.routes import router as comment_router
from modules.user.routers import router as user_router

from core.config import settings

app = FastAPI(
    title="Challenge API",
    description="API for the challenge",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
