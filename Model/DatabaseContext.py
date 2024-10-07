from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DatabaseContext:

    def __init__(self):
        Base = declarative_base()
        self.engine = create_engine(
        )
        engine = self.engine
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(engine)

    def get_session(self):
        return self.Session()

    def close_session(self, session):
        session.close()
