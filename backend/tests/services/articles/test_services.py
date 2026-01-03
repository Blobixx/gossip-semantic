from datetime import datetime, timedelta
from app.services.articles import (
    get_articles_max_published_at,
    get_batch_articles,
    get_relevant_articles,
)
from app.models.Articles import Articles


def test_get_relevant_articles_orders_by_distance(db_session, article_factory):
    # SETUP
    a1 = article_factory(embeddings=[0.0] * 384)
    a2 = article_factory(embeddings=[1.0] * 384)
    a3 = article_factory(embeddings=[10.0] * 384)

    query_embedding = [0.0] * 384

    # ACT
    results = get_relevant_articles(
        session=db_session,
        embedding=query_embedding,
        number_items=3,
    )

    # ASSERT
    assert results[0].uuid == a1.uuid
    assert results[1].uuid == a2.uuid
    assert results[2].uuid == a3.uuid


def test_get_batch_articles(db_session, article_factory):
    # SETUP
    after_published_at = datetime(2022, 4, 7, 10, 0, 0)
    a1 = article_factory(
        embeddings=[0.0] * 384, published_at=after_published_at - timedelta(days=1)
    )
    a2 = article_factory(
        embeddings=[1.0] * 384, published_at=after_published_at + timedelta(days=1)
    )
    a3 = article_factory(
        embeddings=[10.0] * 384, published_at=after_published_at + timedelta(days=10)
    )
    a4 = article_factory(
        embeddings=[10.0] * 384, published_at=after_published_at + timedelta(days=15)
    )

    # ACT
    results = get_batch_articles(
        session=db_session,
        batch_size=2,
        after_published_at=after_published_at,
        order_by="desc",
    )

    # ASSERT
    assert len(results) == 2
    assert results[0].uuid == a4.uuid
    assert results[1].uuid == a3.uuid


def test_get_articles_max_published_at(db_session, article_factory):
    # SETUP
    after_published_at = datetime(2022, 4, 7, 10, 0, 0)
    assert db_session.query(Articles).count() == 0
    a1 = article_factory(
        embeddings=[0.0] * 384, published_at=after_published_at - timedelta(days=1)
    )
    a2 = article_factory(
        embeddings=[1.0] * 384, published_at=after_published_at + timedelta(days=1)
    )
    a3 = article_factory(
        embeddings=[10.0] * 384, published_at=after_published_at + timedelta(days=30)
    )
    a4 = article_factory(
        embeddings=[10.0] * 384, published_at=after_published_at + timedelta(days=15)
    )

    # ACT
    result = get_articles_max_published_at(
        session=db_session,
    )

    # ASSERT
    assert result == a3.published_at
