import os

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Database:
    default_filename = 'database.sqlite'

    def __init__(self, path=default_filename):
        self.path = path

        if os.path.isdir(self.path):
            self.path = os.path.join(self.path, self.default_filename)

        self.engine = create_engine(f'sqlite:///{self.path}')

        Base.metadata.create_all(self.engine)

        self.session_maker = sessionmaker(bind=self.engine)

    def unsuccessful_vfile_exists(self, name: str, hash: str):
        session = self.session_maker()
        exists = session.query(UnsuccessfulFile).filter_by(
            filename=name, hash=hash).first() is not None
        session.close()
        return exists

    def add_unsuccessful_vfile(self, name: str, hash: str, error: str):
        if not self.unsuccessful_vfile_exists(name, hash):
            new_file = UnsuccessfulFile(filename=name, hash=hash, error=error)
            session = self.session_maker()
            session.add(new_file)
            session.commit()
            session.close()

    def add_successful_vfile(self, name: str, hash: str, transfer: str):
        new_file = SuccessfulFile(filename=name, hash=hash, transfer=transfer)
        session = self.session_maker()
        session.add(new_file)
        session.commit()
        session.close()


class UnsuccessfulFile(Base):
    __tablename__ = 'unsuccessful_file'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    hash = Column(String)
    error = Column(String)

    def __repr__(self):
        return f"<UnsuccessfulFile (name='{self.filename}')>"


class SuccessfulFile(Base):
    __tablename__ = 'successful_file'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    hash = Column(String)
    transfer = Column(String)

    def __repr__(self):
        return f"<SuccessfulFile (name='{self.filename}')>"
