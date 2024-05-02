"""
    file : App.API.Student_API.py
    writer : Meohong
    first date : 2024-03-24
    Objective : Student API ( Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-03-24 |   1   |   first write
     2024-04-14 |   2   |   Optimize Code
     2024-05-03 |   3   |   change that login token is not necessary for save student data
    ========================================================================
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing_extensions import Annotated
from App.Service.Student_Service import StudentService
from App.Service.user_Service import UserService
from App.database.repository import UserRepository, StudentRepository
from App.api.user_API import oauth2_scheme
from App.Schema import student_schema

app = APIRouter(
    prefix="/student",
)

student_service = Annotated[StudentService, Depends()]
student_repository = Annotated[StudentRepository, Depends()]
user_service = Annotated[UserService, Depends()]
user_repository = Annotated[UserRepository, Depends()]

@app.get("/get_student")
async def get_student(
        login_token: Annotated[str, Depends(oauth2_scheme)],
        student_serv: student_service,
        student_repo: student_repository,
        user_serv: user_service,
        user_repo: user_repository,
):
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid")

    user_id = user_serv.get_user(email=user_email, user_repo=user_repo).id
    user_student = student_serv.get_student(user_id=user_id, student_repo=student_repo)
    if not user_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student data not found")
    return user_student

@app.post("/save_student")
async def save_student(
        student_serv: student_service,
        student_repo: student_repository,
        user_serv: user_service,
        user_repo: user_repository,
        user_email: str,
        new_student: student_schema.StudentForm = Depends(),
):
    try:
        if user_email is None:
            raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_UNAUTHORIZED, detail="No User Email")

    # 로그인 정보에서 유저의 아이디를 얻어옴
    user_id = user_serv.get_user(email=user_email,user_repo=user_repo).id
    already_exist = student_serv.get_student(user_id=user_id, student_repo=student_repo) # 이미 학생 데이터가 있는지 확인
    if already_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already exists")
    # 데이터 저장
    student = student_serv.save_student(user_id=user_id, new_student=new_student, student_repo=student_repo)
    if student is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No Student information")
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Student data Success")

@app.delete("/delete_student")
async def delete_student(
        login_token: Annotated[str, Depends(oauth2_scheme)],
        student_serv: student_service,
        student_repo: student_repository,
        user_serv: user_service,
        user_repo: user_repository,
):
    # 로그인된 상태를 확인
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    # 로그인 상태가 아님
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid")

    # 로그인 정보에서 유저의 아이디를 얻어옴
    user_id = user_serv.get_user(email=user_email,user_repo=user_repo).id
    # 데이터 삭제
    return_number = student_serv.delete_student(user_id=user_id, student_repo=student_repo)
    if return_number != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student data not found")
    return HTTPException(status_code=status.HTTP_200_OK, detail="Student deleted")


@app.patch("/modify_student")
async def modify_student(
        student_serv: student_service,
        student_repo: student_repository,
        user_serv: user_service,
        user_repo: user_repository,
        login_token: Annotated[str, Depends(oauth2_scheme)],
        update_form: student_schema.StudentForm = Depends(),
):
    # 로그인된 상태를 확인
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    # 로그인 상태가 아님
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid")

    # 로그인 정보에서 유저의 아이디를 얻어옴
    renew_user_id = user_serv.get_user(email=user_email, user_repo=user_repo).id
    if renew_user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not exists")
    # 수정할 학생 정보를 가져옴
    renew_student = student_serv.get_student(user_id=renew_user_id, student_repo=student_repo)
    # 결과값 반환
    return_number = student_serv.update_student(user_id=renew_user_id, update_form=update_form, student=renew_student, student_repo=student_repo)
    if return_number != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student data is Not updated")
    return HTTPException(status_code=status.HTTP_200_OK, detail="Student updated")
