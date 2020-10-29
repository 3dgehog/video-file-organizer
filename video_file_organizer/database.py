import os

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Database:
    default_filename = 'store.sqlite'

    def __init__(self, path=default_filename):
        self.path = path

        if os.path.isdir(self.path):
            self.path = os.path.join(self.path, self.default_filename)

        self.engine = create_engine(f'sqlite:///{self.path}')

        Base.metadata.create_all(self.engine)

        self.session_maker = sessionmaker(bind=self.engine)

    def hash_name_pair_exists(self, name: str, hash: str):
        session = self.session_maker()
        exists = session.query(File).filter_by(
            filename=name, hash=hash).first() is not None
        session.close()
        return exists

    def add_hash_name_pair(self, name: str, hash: str, error: str):
        if not self.hash_name_pair_exists(name, hash):
            new_file = File(filename=name, hash=hash, error=error)
            session = self.session_maker()
            session.add(new_file)
            session.commit()
            session.close()


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    hash = Column(String)
    error = Column(String)

    def __repr__(self):
        return f"<File (name='{self.filename}')>"
