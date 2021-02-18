from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

DEFAULT_FILENAME = 'database.sqlite'

engine = create_engine(f'sqlite:///{DEFAULT_FILENAME}')

db_session = scoped_session(sessionmaker(
    bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
