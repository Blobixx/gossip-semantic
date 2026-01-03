from pydantic import BaseModel


class ArticleSearchInput(BaseModel):
    query: str
