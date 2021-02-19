from . import Base, db_session, engine
from .models import UnsuccessfulFile, SuccessfulFile


def init_db():
    Base.metadata.create_all(engine)


def unsuccessful_vfile_exists(name: str, hash: str):
    exists = db_session.query(UnsuccessfulFile).filter_by(
        filename=name, hash=hash).first() is not None
    db_session.close()
    return exists


def add_unsuccessful_vfile(name: str, hash: str, error: str):
    if not unsuccessful_vfile_exists(name, hash):
        new_file = UnsuccessfulFile(filename=name, hash=hash, error=error)
        db_session.add(new_file)
        db_session.commit()
        db_session.close()


def add_successful_vfile(name: str, hash: str, transfer: str):
    new_file = SuccessfulFile(filename=name, hash=hash, transfer=transfer)
    db_session.add(new_file)
    db_session.commit()
    db_session.close()


def get_unsuccessful_vfiles():
    response = db_session.query(UnsuccessfulFile).all()
    return response
