

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from ..database.connection import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    regdate = Column(DateTime, nullable=False, default=datetime.now)

    # 클래스 매서드를 만들어 인스턴스를 만들지 않고 객체를 생성할 수 있음
    @classmethod
    def create(cls, name:str, email:str, password:str) -> "User":
       return cls(
           name=name,
           email=email,
           password=password
       )

class ImagePATH(Base):
    __tablename__ = "image"

    imageid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    makerid = Column(Integer, primary_key=True, nullable=False)
    imagename = Column(String, nullable=False)
    imagepath = Column(String, nullable=False)
    makedate = Column(DateTime, nullable=False, default=datetime.now)

    @classmethod
    def create(cls, makerid:int, imagename: str,imagepath: str) -> "ImagePATH":
        return cls(
            makerid=makerid,
            imagename=imagename,
            imagepath=imagepath,
        )

class Student(Base):
    __tablename__ = "student"

    studentid = Column(Integer, primary_key=True, nullable=False)
    userid = Column(Integer, primary_key=True, nullable=False)
    univ = Column(String, nullable=False)
    major = Column(String, nullable=False)

    @classmethod
    def create(cls, studentid: int, userid: int, univ: str, major: str):
        return cls(
            studentid=studentid,
            userid=userid,
            univ=univ,
            major=major,
        )