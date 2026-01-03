from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Articles import Articles


def get_articles_max_published_at(*, session: Session) -> datetime | None:
    query = select(Articles).order_by(Articles.published_at.desc())

    last_published_article = session.execute(query).scalars().first()
    if last_published_article is None:
        return None

    return last_published_article.published_at


def get_batch_articles(
    *,
    session: Session,
    batch_size: int,
    order_by: str | None = None,
    without_embeddings_only: bool | None = None,
    after_published_at: datetime | None = None,
) -> list[Articles]:
    query = select(Articles)

    if after_published_at is not None:
        query = query.where(Articles.published_at > after_published_at)

    if order_by is not None:
        if order_by == "desc":
            query = query.order_by(Articles.published_at.desc())
        else:
            query = query.order_by(Articles.published_at.asc())

    if without_embeddings_only:
        query = query.where(Articles.embeddings.is_(None))

    return session.execute(query.limit(batch_size)).scalars().all()


def get_relevant_articles(
    *, session: Session, embedding: list, number_items: int
) -> list[Articles]:
    query = (
        select(Articles)
        .where(Articles.embeddings.is_not(None))
        .order_by(Articles.embeddings.op("<=>")(embedding))
        .limit(number_items)
    )

    return list(session.execute(query).scalars().all())
