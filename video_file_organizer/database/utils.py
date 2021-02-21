from . import Base, Session, engine
from .models import UnsuccessfulFile, SuccessfulFile


def init_db():
    Base.metadata.create_all(engine)


def unsuccessful_vfile_exists(name: str, hash: str):
    session = Session()
    exists = session.query(UnsuccessfulFile).filter_by(
        filename=name, hash=hash).first() is not None
    Session.remove()
    return exists


def add_unsuccessful_vfile(name: str, hash: str, error: str):
    if not unsuccessful_vfile_exists(name, hash):
        new_file = UnsuccessfulFile(filename=name, hash=hash, error=error)
        session = Session()
        session.add(new_file)
        session.commit()
        Session.remove()


def add_successful_vfile(name: str, hash: str, transfer: str):
    new_file = SuccessfulFile(filename=name, hash=hash, transfer=transfer)
    session = Session()
    session.add(new_file)
    session.commit()
    Session.remove()


def get_unsuccessful_vfiles():
    session = Session()
    response = session.query(UnsuccessfulFile).all()
    Session.remove()
    return response
