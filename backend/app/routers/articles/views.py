from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.embedding_model import embedding_model
from app.routers.dependencies import get_db
from app.routers.articles.inputs import ArticleSearchInput
from app.services.articles import get_relevant_articles
from app.routers.articles.types import ApiArticle

articles_router = APIRouter()


@articles_router.post("/articles/search", response_model=list[ApiArticle])
def get_articles(
    input: ArticleSearchInput, db: Session = Depends(get_db)
) -> list[ApiArticle]:
    query_embedding = embedding_model.encode(
        input.query,
        normalize_embeddings=True,  # important for cosine similarity
    ).tolist()

    articles = get_relevant_articles(
        session=db, embedding=list(query_embedding), number_items=5
    )

    return [
        ApiArticle(
            site_name=article.site_name,
            author=article.author,
            published_at=article.published_at,
            content=article.content,
            description=article.description,
            title=article.title,
        )
        for article in articles
    ]
