"""
    file : App.database.repository.py
    writer : Meohong
    first date : 2024-02-21
    Objective : To manage DB Table ( CRUD operations )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-02-21 |   1   |   first write
     2024-03-18 |   2   |   ImagePATH repository write
     2024-03-24 |   3   |   student repository write
     2024-04-14 |   4   |   Account, Mydata repository write
    ========================================================================
"""

from typing import List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from App.database.connection import get_db
from App.database.tables import User, Student, Account, Mydata

""" 
    각 데이터베이스 테이블 당 Repository를 만들어 각각에 대한 CRUD를 설정하자.
    이렇게 하는 이유: 각 서비스마다 분리시켜 한눈에 알아볼 수 있게 하기 위함
"""

class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session

    # 데이터베이스 테이블 안의 모든 유저들의 데이터를 모두 끌고 온다.

    def get_users(self) -> List[User]:
        return list(self.db.execute(select(User)).scalars())

    # 특정한 조건을 갖춘 데이터를 얻는 함수
    def get_user_by_email(self, email: str) -> User:
        return self.db.execute(
            select(User).where(User.email == email)
        ).scalar()

    # 데이터베이스 스키마에 데이터를 저장하는 함수
    def save_user(self, user: User) -> User.id:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user.id

    # 데이터베이스 스키마 안의 특정 번호의 데이터를 삭제하는 함수
    def delete_user(self, user_id: int) -> None:
        self.db.execute(
            delete(User).where(User.id == user_id)
        )
        self.db.commit()

    # 특정 유저의 데이터베이스 업데이트
    def update_user(self, update_user: User) -> User:
        self.db.add(update_user)
        self.db.commit()
        self.db.refresh(update_user)
        return update_user

class StudentRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session

    # 학생 정보를 얻는 함수
    def get_student_info(self, user_id: int):
        return self.db.execute(select(Student).where(Student.userid == user_id)).scalar()

    def delete_student_info(self, user_id: int):
        self.db.execute(
            delete(Student).where(Student.userid == user_id)
        )
        self.db.commit()

    def save_student_info(self, student:Student) -> Student.studentid:
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student.studentid

    def update_student_info(self, student:Student) ->Student.studentid:
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student.studentid

class AccountRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session

    # 한 사람의 계좌 정보들을 모두 가져옴
    def get_account_by_user_id(self, user_id: int) -> List[Account]:
        return list(
            self.db.execute(
                select(Account).where(Account.user_id == user_id)
            ).scalars()
        )

    # 새로운 계좌정보를 삽입
    def save_account(self, account: Account) -> Account.id:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account.id

    # 계좌정보를 삭제
    def delete_account(self, account_id: int) -> None:
        self.db.execute(
            delete(Account).where(Account.id == account_id)
        )
        self.db.commit()

class MydataRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session

    # 계좌 정보 가져오기
    def get_datas_by_account_id(self, account_id: int) -> List[Mydata]:
        return list(
            self.db.execute(
                select(Mydata).where(Mydata.account_id == account_id)
            ).scalars()
        )
    # 계좌 정보 입력
    def save_mydata(self, mydata: Mydata) -> None:
        self.db.add(mydata)
        self.db.commit()
        self.db.refresh(mydata)

    def delete_mydata_by_account_id(self, account_id: int) -> None:
        self.db.execute(
            delete(Mydata).where(Mydata.account_id == account_id)
        )
        self.db.commit()

    def delete_mydata_by_clients(self, clients: str) -> None:
        self.db.execute(
            delete(Mydata).where(Mydata.clients == clients)
        )
        self.db.commit()
