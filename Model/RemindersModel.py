from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Reminders(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    chanelId = Column(Integer, nullable=False)

    committeeSitting = Column(Date, nullable=False)
    platform = Column(String, nullable=False)

    def __repr__(self):
        return f"<Chanel(id={self.id}, chanelId={self.chanelId}, committeeSitting={self.committeeSitting},platform={self.platform})>"
