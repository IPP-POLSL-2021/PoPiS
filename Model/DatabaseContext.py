from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseContext:
    def __init__(self):
        self.engine = create_engine(
            'postgresql://c179:C577_aee233@psql01.mikr.us/db_c179')  # Ustaw dane połączenia
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def close_session(self, session):
        session.close()
