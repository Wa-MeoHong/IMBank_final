"""
    file : App.Service.user_Service.py
    writer : Meohong
    first date : 2024-02-21
    Objective : User Service ( Actually User Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-02-21 |   1   |   first write
     2024-02-21 |   2   |   modify and improve code
     2024-02-22 |   3   |   Classization,  Optimize

    ========================================================================
"""

from datetime import timedelta, datetime, timezone
from typing import Union

from fastapi import HTTPException
from jose import jwt, JWTError

from App.Schema.token_schema import TokenData
from App.database.tables import User
from App.database.repository import UserRepository
from App.Schema.user_schema import UserForm
from passlib.context import CryptContext
from App.Security.config import jwt_setting

class UserService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.jwt_set = jwt_setting()

    def is_exist_user_by_email(self, email: str, user_repo: UserRepository) -> bool:
        user = user_repo.get_user_by_email(email=email)
        return user is not None

    # User Data를 얻는다. 이 때 동일한 이메일인지 확인한다.
    def get_user(self, email: str, user_repo: UserRepository) -> User:
        user = user_repo.get_user_by_email(email=email)
        return user

    # User Data 입력하기
    def create_user(self, new_user: UserForm, user_repo: UserRepository):
        # 입력받은 JSON을 토대로 새롭게 객체를 생성
        password = new_user.password.get_secret_value()
        user = User.create(
            name=new_user.name,
            email=new_user.email,
            password=self.pwd_context.hash(password)
        )
        user_repo.save_user(user=user)
        return HTTPException(status_code=201, detail=f"User created successfully")

    # User 데이터를 삭제하는 함수
    def delete_user(self, user_id: int, user_repo: UserRepository):
        # 삭제할 유저의 고유 번호를 가지고 삭제를 진행
        user_repo.delete_user(user_id=user_id)
        return HTTPException(status_code=200, detail=f"User deleted successfully")

    # User 데이터 업데이트 하는 함수
    def update_user(self, update_form: UserForm, user: User, user_repo: UserRepository):
        # 가져온 user 데이터를 수정한다.
        # 비밀번호 수정
        password = update_form.password.get_secret_value()
        user.name = update_form.name
        user.password = self.pwd_context.hash(password)

        # 똑같은 기본키를 가지고 있다면 내용이 수정된다.
        user_repo.save_user(user)
        return HTTPException(status_code=200, detail=f"User updated successfully")

    # 비밀번호 복호화 폼
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    # JWT 토큰 생성 폼
    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()  # 인코딩할 데이터를 가져옴
        # 디폴트: 30분만 로그인, 만약 설정값이 들어온다면 설정값을 사용
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=self.jwt_set.ACCESS_TOKEN_EXPIRE_MINUTES)  # 현재 시각에서 30분까지
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, key=self.jwt_set.JWT_KEY, algorithm=self.jwt_set.ALGORITHM)
        return encoded_jwt  # 토큰 반환

    # JWT 토큰 디코딩
    def decode_access_token(self, access_token: str) -> str:
        try:
            payload: dict = jwt.decode(access_token, key=self.jwt_set.JWT_KEY, algorithms=self.jwt_set.ALGORITHM)
            user_email: str = payload["email"]
            if user_email is None:
                raise HTTPException(status_code=404, detail="User Not Found")
            return user_email
        except JWTError:
            raise HTTPException(status_code=401, detail="Not Authorized", headers={"WWW-Authenticate": "Bearer"})


"""
jwt_setting = jwt_setting()
# 비밀번호 암호화 해싱을 위한 인코더
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def is_exist_user_by_email(
        email: str,
        user_repo: UserRepository
) -> bool:
    user = user_repo.get_user_by_email(email=email)
    return user is not None


# User Data를 얻는다. 이 때 동일한 이메일인지 확인한다.
def get_user(
        email: str,
        user_repo: UserRepository
):
    user = user_repo.get_user_by_email(email=email)
    return user

# User Data 입력하기
def create_user(
        new_user: UserForm,
        user_repo: UserRepository
):
    # 입력받은 JSON을 토대로 새롭게 객체를 생성
    user = User.create(
        name=new_user.name,
        email=new_user.email,
        password=pwd_context.hash(new_user.password)
    )

    # db에 추가하고 커밋
    user_repo.save_user(user=user)
    return HTTPException(status_code=200, detail=f"User created successfully")

# User 데이터를 삭제하는 함수
def delete_user(
        user_id: int,
        user_repo: UserRepository
):
    # 삭제할 유저의 고유 번호를 가지고 삭제를 진행
    user_repo.delete_user(user_id=user_id)
    return HTTPException(status_code=200, detail=f"User deleted successfully")

# User 데이터 업데이트 하는 함수
def update_user(
        update_form: UserForm,
        user: User,
        user_repo: UserRepository
):
    # 가져온 user 데이터를 수정한다.
    user.name = update_form.name
    user.password = pwd_context.hash(update_form.password)

    # 똑같은 기본키를 가지고 있다면 내용이 수정된다.
    user_repo.save_user(user)
    return HTTPException(status_code=200, detail=f"User updated successfully")

# 비밀번호 복호화 폼
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT 토큰 생성 폼
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None ):
    to_encode = data.copy()     # 인코딩할 데이터를 가져옴
    # 디폴트: 30분만 로그인, 만약 설정값이 들어온다면 설정값을 사용
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=jwt_setting.ACCESS_TOKEN_EXPIRE_MINUTES) # 현재 시각에서 30분까지
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=jwt_setting.SECRET_KEY, algorithm=jwt_setting.Algorithm)
    return encoded_jwt # 토큰 반환

def successful_response(status_code: int):
    return {
        'status_code': status_code,
        'transaction': "Successful"
    }

"""