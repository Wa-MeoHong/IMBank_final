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
    ========================================================================
"""

from typing import List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from App.database.connection import get_db
from App.database.tables import User, ImagePATH, Student

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
    def update_user(self, update_user:User) -> User:
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
