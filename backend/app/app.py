from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.articles.views import articles_router

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.include_router(articles_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
