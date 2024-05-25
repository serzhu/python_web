import os
from  pathlib import Path

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1].joinpath('.env'))
URI = os.environ.get('DATABASE_URL')
engine = create_engine(URI)
Session = sessionmaker(autocommit=False, autoflush=False,bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()