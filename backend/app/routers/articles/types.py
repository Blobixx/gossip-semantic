from datetime import datetime
from pydantic import BaseModel


class ApiArticle(BaseModel):
    site_name: str
    author: str
    title: str
    published_at: datetime
    content: str
    description: str
