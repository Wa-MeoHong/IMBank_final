

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

class Student(Base):
    __tablename__ = "student"

    studentid = Column(Integer, primary_key=True, nullable=False)
    userid = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)
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

# 계좌 정보를 담고있는 테이블
class Account(Base):
    __tablename__ = "account"

    # 테이블 속성
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)
    accountnum = Column(String, nullable=False)
    objective = Column(String, nullable=False)

    @classmethod
    def create(cls, user_id: int, account_num: str, objective: str):
        return cls(
            user_id=user_id,
            accountnum=account_num,
            objective=objective,
        )
# 계좌 거래내역을 담고있는 테이블
class Mydata(Base):
    __tablename__ = "dealhist"

    account_id = Column(Integer, ForeignKey("account.id"), primary_key=True, nullable=False)
    clients = Column(String, nullable=False)
    dealcost = Column(Integer, nullable=False)
    leftcharge = Column(Integer, nullable=False)
    dealtime = Column(DateTime, nullable=False)
    dealtype = Column(String, nullable=False)

    @classmethod
    def create(cls, account_id: int, clients: str, dealcost: int, leftcharge: int, dealtime: DateTime, dealtype: str):
        return cls(
            account_id=account_id,
            clients=clients,
            dealcost=dealcost,
            leftcharge=leftcharge,
            dealtime=dealtime,
            dealtype=dealtype
        )

