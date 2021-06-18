from loggingconfig import getLogger
log = getLogger(__name__)

from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from datetime import datetime, timedelta
import config

log.debug("Creating engine.")
engine = create_engine('sqlite:///app.db', echo=False, connect_args={'check_same_thread': False})
log.debug("Creating declarative base")
base = declarative_base(bind=engine)
log.debug("Creating metadata.")
metadata = base.metadata
log.debug("Creating session.")
session = scoped_session(sessionmaker(bind=engine))


class Model(): 
    
    def commit(self):
        try:
            session.add(self)
            log.debug(f'Commited {self.__repr__()}')
        except:
            session.rollback()
        else:
            session.commit()
        return self

    def delete(self):
        try:
            session.delete(self)
            log.debug(f'Deleted {self.__repr__()}')
        except:
            session.rollback()
        else:
            session.commit()
        return self


class User(base, Model):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    tg_id = Column(Integer, unique=True, nullable=False)
    tg_username = Column(String)
    cords_id = Column(ForeignKey('cords.id'))
    sent_photos = Column(Integer, nullable=False, default=0)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    cords = relationship('Cords')
    
    def __init__(self, tg_id, tg_username, chat_id):
        self.tg_id = tg_id
        self.tg_username = tg_username
        self.chat_id = chat_id
        
        log.debug(f'Initializated {self.__repr__()}')
        
    def __repr__(self):
        return f'<User username={self.tg_username}, created={self.created}>'
    
    def setCords(self, latitude, longitude):
        latitude_ref = 'N' if latitude >= 0 else 'S'
        longitude_ref = 'E' if longitude >= 0 else 'W'
        cords = Cords(
            abs(latitude),
            abs(longitude),
            latitude_ref,
            longitude_ref
        ).commit()
        self.cords = cords
        self.commit()
    
def getUser(id):
    return session.query(User).get(id)

def getUserByTg(tg_id):
    return session.query(User).filter_by(tg_id=tg_id).first()
    
    
class Cords(base, Model):
    __tablename__ = 'cords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)
    latitude_ref = Column(String)
    longitude_ref = Column(String)
    updated = Column(DateTime, nullable=False, default=datetime.utcnow)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, latitude, longitude, latitude_ref, longitude_ref):
        self.latitude = latitude
        self.longitude = longitude
        self.latitude_ref = latitude_ref
        self.longitude_ref = longitude_ref
        
        log.debug(f'Initializated {self.__repr__()}')

    def __repr__(self):
        return f'<Cords latitude={self.latitude} {self.latitude_ref}, \
longitude={self.longitude} {self.longitude_ref}, created={self.created}>'

    def getTelegramTypeCords(self):
        latitude = -self.latitude if self.latitude_ref == 'S' else self.latitude
        longitude = -self.longitude if self.longitude_ref == 'W' else self.longitude
        return latitude, longitude