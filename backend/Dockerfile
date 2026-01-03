FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENV=dev

WORKDIR /backend

# Install build deps (psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*


# Install uv (Uvicorn) and dependencies
COPY pyproject.toml .
RUN pip install --upgrade pip uv && uv sync

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY tests ./tests

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]

