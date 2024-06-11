from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()

job_category_association = Table('job_category_association', Base.metadata,
                                 Column('job_id', Integer,
                                        ForeignKey('jobs.id')),
                                 Column('category_id', Integer,
                                        ForeignKey('categories.id'))
                                 )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    name = Column(String)
    age = Column(Integer)
    position = Column(String)
    speciality = Column(String)
    address = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    modified_date = Column(DateTime)


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    job = Column(String)
    team_leader = Column(Integer)
    work_size = Column(Integer)
    collaborators = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_finished = Column(Boolean)
    categories = relationship(
        "Category", secondary=job_category_association, back_populates="jobs")


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    jobs = relationship(
        "Job", secondary=job_category_association, back_populates="categories")


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    chief = Column(Integer, ForeignKey('users.id'))
    members = Column(String)  # Хранение списка ID в виде строки
    email = Column(String, unique=True)

    chief_user = relationship("User", foreign_keys=[chief])


engine = create_engine('sqlite:///mars_explorer.db')
Base.metadata.create_all(engine)
