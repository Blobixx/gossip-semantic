#!/usr/bin/env python3

# Script to compute and store embeddings for articles without embeddings in the database.
# The embeddings are computed in batches and stored back in the database.
# The embeddings are base on embedding_model defined in app/embedding_model.py
# The embeddings are computed using the content of the articles.

from datetime import datetime
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Now imports will work
from app.services.articles import (
    get_articles_max_published_at,
    get_batch_articles,
)
from app.database import DATABASE_URL
from app.embedding_model import embedding_model
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def run():
    engine = create_engine(DATABASE_URL)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    print(f"Start of embeddings computation")
    batch_size = 100
    batch_number = 0
    after_published_at = datetime.min

    max_published_at = get_articles_max_published_at(session=session)
    if max_published_at is None:
        print("No articles found in the database.")
        return

    while after_published_at < max_published_at:
        articles = get_batch_articles(
            session=session,
            batch_size=batch_size,
            after_published_at=after_published_at,
            without_embeddings_only=True,
            order_by="asc",
        )

        if len(articles) == 0:
            print("No articles without embeddings found. Exiting.")
            break

        print(f"Processing batch number {batch_number} of size {len(articles)}")

        update_data = {}
        for article in articles:
            if article.embeddings is not None:
                continue
            embedding = embedding_model.encode(
                article.content,
                normalize_embeddings=True,  # important for cosine similarity
            ).tolist()
            update_data[article.uuid] = embedding

        for uuid, embedding_vector in update_data.items():
            session.execute(
                text(
                    """
                    UPDATE articles
                    SET embeddings = :embedding
                    WHERE uuid = :uuid;
                """
                ).bindparams(embedding=embedding_vector, uuid=uuid)
            )

        session.commit()

        print(f"Batch number {batch_number} processed.")
        after_published_at = articles[-1].published_at
        batch_number += 1


if __name__ == "__main__":
    run()
