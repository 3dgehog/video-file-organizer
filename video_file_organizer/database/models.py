from sqlalchemy import Column, Integer, String

from . import Base


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
