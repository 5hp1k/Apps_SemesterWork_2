from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    surname = Column(String(50))
    name = Column(String(50))
    age = Column(Integer)
    email = Column(String(100), unique=True)
    hashed_password = Column(String)
    modified_date = Column(DateTime)

    images = relationship('Image', back_populates='author_user')
    votes = relationship('Vote', back_populates='user')


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(Integer, ForeignKey('users.id'))
    prompt = Column(String)
    generation_date = Column(DateTime)
    rating = Column(Integer, default=0)

    author_user = relationship("User", back_populates="images")
    votes = relationship("Vote", back_populates="image")


class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    image_id = Column(Integer, ForeignKey('images.id'))
    vote_type = Column(String)

    user = relationship("User")
    image = relationship("Image")

    __table_args__ = (UniqueConstraint(
        'user_id', 'image_id', name='_user_image_uc'),)


engine = create_engine('sqlite:///app_database.db')
Base.metadata.create_all(engine)
