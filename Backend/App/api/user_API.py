"""
    file : App.api.user_API.py
    writer : Meohong
    first date : 2024-02-21
    Objective : User API ( Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-02-21 |   1   |   first write
     2024-02-21 |   2   |   modify and improve code
     2024-02-21 |   3   |   Include Login, Service Class Optimize
     2024-04-14 |   4   |   Optimize Code
     2024-05-03 |   5   |   Add get userdata method
    ========================================================================
"""
from datetime import datetime, timedelta, timezone
from fastapi import Response, Request
from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from App.Schema import user_schema, token_schema
from fastapi import HTTPException, status
import json

from App.Security.config import jwt_setting
from App.Service.user_Service import UserService
from App.database.repository import UserRepository

jwt_set = jwt_setting()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login", scheme_name="JWT",
    description="인증이 필요한 API를 호출하기 위해 로그인을 해주세요."
)
user_repository = Annotated[UserRepository, Depends()]
user_service = Annotated[UserService, Depends()]

app = APIRouter(
    prefix="/user",
)

"""로그인 폼"""
@app.post("/login")
async def user_login(
        user_repo: user_repository,
        user_serv: user_service,
        login_form: OAuth2PasswordRequestForm = Depends()
):
    is_exist = user_serv.is_exist_user_by_email(email=login_form.username, user_repo=user_repo)
    if not is_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")

    user = user_serv.get_user(email=login_form.username, user_repo=user_repo)
    res = user_serv.verify_password(plain_password=login_form.password, hashed_password=user.password)
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")

    # 토큰 생성
    access_token = user_serv.create_access_token(data={"email": user.email})
    print(access_token)
    return token_schema.Token(access_token=access_token, token_type="bearer")

"""회원가입 폼"""
@app.post("/signup")
async def user_signup(
        user_serv: user_service,
        user_repo: user_repository,
        new_user: Annotated[user_schema.UserForm, Depends()],
):
    # 먼저 유저를 입력 하여 데이터셋으로 만듦
    user = user_serv.get_user(email=new_user.email, user_repo=user_repo)

    # 만약 그 유저가 이미 데이터베이스에 존재한다면 바로 오류를 출력
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    # 아니면 유저 제작
    user = user_serv.create_user(new_user=new_user, user_repo=user_repo)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Signup Succeed")

#회원 정보 조회
@app.get("/userdata")
async def get_user_data(
        user_serv: user_service,
        user_repo: user_repository,
        token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        user_email = user_serv.decode_access_token(token)
        if user_email is None:
            raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    user = user_serv.get_user(email=user_email, user_repo=user_repo)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not exists")

    user_json = {
        "name": user.name,
        "email": user.email
    }

    return user_json

""" 회원 삭제 폼"""
@app.delete("/resign")
async def user_resign(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_serv: user_service,
        user_repo: user_repository,
):
    try:
        user_email = user_serv.decode_access_token(token)
        if user_email is None:
            raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    # 회원삭제를 위해 먼저 회원이 존재 하는지 확인
    remove_user = user_serv.get_user(email=user_email, user_repo=user_repo)
    # 회원이 존재하지 않는다면 오류를 출력
    if remove_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not exists")

    # 통과 하면 삭제를 진행
    user_serv.delete_user(user_id=remove_user.id, user_repo=user_repo)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Resign Succeed")


"""회원 정보 수정"""
""" OAuth를 이용하여 유저 확인을 한 후 인증이 된 토큰을 확인 되면 수정"""
@app.patch("/update")
async def user_update(
        user_serv: user_service,
        user_repo: user_repository,
        token: Annotated[str, Depends(oauth2_scheme)],
        update_user: user_schema.UserForm = Depends(),
):
    try:
        user_email = user_serv.decode_access_token(access_token=token)
        if user_email is None:
            raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")

    # 먼저 데이터가 존재하는지 살펴봄, 존재하지 않는 회원이라면 오류를 출력
    renew_user = user_serv.get_user(email=update_user.email, user_repo=user_repo)
    if renew_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not exists")
    # 업데이트 작업을 진행
    user_serv.update_user(update_form=update_user, user=renew_user, user_repo=user_repo)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Update Succeed")