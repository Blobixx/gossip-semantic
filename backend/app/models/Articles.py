from datetime import datetime
from sqlalchemy import UUID, Column, DateTime, String
from ..database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from pgvector.sqlalchemy import VECTOR


# Based on embedding model used
VECTOR_SIZE = 384


class Articles(Base):
    __tablename__ = "articles"

    uuid: Mapped[UUID] = Column(UUID, primary_key=True)
    site_name: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    content: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    embeddings = mapped_column(VECTOR(384), nullable=True)
