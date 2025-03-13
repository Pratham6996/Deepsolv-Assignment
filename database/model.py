from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import datetime

username = "root"
password = "18052310"  
host = "localhost"
database = "linkedin_insights"

engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}/{database}", echo=True)


Base = declarative_base()

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    linkedin_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    profile_picture = Column(String(500))
    description = Column(Text)
    website = Column(String(500))
    industry = Column(String(255))
    followers = Column(Integer)
    headcount = Column(Integer)
    specialties = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    posts = relationship("Post", back_populates="page")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer, ForeignKey('pages.id'), nullable=False)
    content = Column(Text, nullable=False)
    post_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    page = relationship("Page", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    post = relationship("Post", back_populates="comments")

class SocialMediaUser(Base):
    __tablename__ = 'social_media_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    linkedin_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    profile_url = Column(String(500))
    job_title = Column(String(255))
    company = Column(String(255))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
