"""
    file : App.Service.Student_Service.py
    writer : Meohong
    first date : 2024-03-24
    Objective : Student Service ( Actually Student Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-03-24 |   1   |   first write

    ========================================================================
"""

from fastapi import HTTPException, status
from typing import Union
from jose import jwt, JWTError

from App.database.tables import User, Student
from App.database.repository import UserRepository, StudentRepository
from App.Schema.student_schema import StudentForm

class StudentService:
    def __init__(self):
        self.initialize = 1

    def get_student(self, user_id: int, student_repo: StudentRepository) -> Student:
        student = student_repo.get_student_info(user_id=user_id)
        return student if student else None

    def save_student(self, user_id: int, new_student: StudentForm, student_repo:StudentRepository) -> Student:
        student = Student.create(
            studentid=new_student.student_id,
            userid=user_id,
            univ=new_student.university_name,
            major=new_student.major
        )
        student_repo.save_student_info(student=student)
        return student

    def delete_student(self, user_id: int, student_repo:StudentRepository):
        remove_student = student_repo.get_student_info(user_id=user_id)
        if not remove_student:
            return 404
        student_repo.delete_student_info(user_id=user_id)
        return 200


    def update_student(self, user_id: int, update_form: StudentForm, student:Student, student_repo:StudentRepository):
        if not user_id:
            return 404
        student.major = update_form.major
        student.univ = update_form.university_name
        student.studentid = update_form.student_id
        student_repo.update_student_info(student=student)
        return 200