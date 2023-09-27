from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Float, create_engine, func
from sqlalchemy.orm import Session, declarative_base,relationship,validates

DATABASE_URL = 'sqlite:///mydatabase.db'

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artist_table'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)

class Song(Base):
    __tablename__ = 'songs_table'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_Date = Column(Text)
    bpm = Column(Integer)
    artist_id = Column(Integer,ForeignKey('artist_table.id'))
    artist = relationship('Artist',backref = "songs")

Base.metadata.create_all(engine)

session.close()
