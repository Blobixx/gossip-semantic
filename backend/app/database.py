from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Load .env from the backend/ folder
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)

DATABASE_URL_PREFIX = os.getenv("DATABASE_URL_PREFIX", None)

if DATABASE_URL_PREFIX is None:
    raise ValueError("DATABASE_URL_PREFIX environment variable is not set")

DATABASE_NAME = os.getenv("DATABASE_NAME", None)

if DATABASE_NAME is None:
    raise ValueError("DATABASE_NAME environment variable is not set")

engine = create_engine(f"{DATABASE_URL_PREFIX}/{DATABASE_NAME}")
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
