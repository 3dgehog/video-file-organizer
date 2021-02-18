from . import Base, db_session, engine
from .models import UnsuccessfulFile, SuccessfulFile


def init_db():
    Base.metadata.create_all(engine)


class Database:
    def __init__(self):
        init_db()

    def unsuccessful_vfile_exists(self, name: str, hash: str):
        exists = db_session.query(UnsuccessfulFile).filter_by(
            filename=name, hash=hash).first() is not None
        db_session.close()
        return exists

    def add_unsuccessful_vfile(self, name: str, hash: str, error: str):
        if not self.unsuccessful_vfile_exists(name, hash):
            new_file = UnsuccessfulFile(filename=name, hash=hash, error=error)
            db_session.add(new_file)
            db_session.commit()
            db_session.close()

    def add_successful_vfile(self, name: str, hash: str, transfer: str):
        new_file = SuccessfulFile(filename=name, hash=hash, transfer=transfer)
        db_session.add(new_file)
        db_session.commit()
        db_session.close()
