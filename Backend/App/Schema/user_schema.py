from pydantic import BaseModel, EmailStr, field_validator, SecretStr
from fastapi import HTTPException

class UserForm(BaseModel):
    # 회원가입을 위한 용도의 폼
    name: str
    email: EmailStr
    password: SecretStr

    # 유효성 검사를 진행하는 곳 (비어있는 칸이 있으면 확인)
    @field_validator('name', 'email')
    def check_empty(self, value):
        if not value or value.isspace():
            raise HTTPException(status_code=422, detail="필수 항목을 입력 하세요.")
        return value

    @field_validator('password')
    def check_password_empty(self, value):
        password = value.get_secret_value()
        if not password or password.isspace():
            raise HTTPException(status_code=422, detail="필수 항목을 입력 하세요.")
        return value

    # 패스워드 8자리 이상 확인 및 영문 숫자 입력 확인
    @field_validator('password')
    def check_password(self, value):
        password = value.get_secret_value()
        if len(password) < 8:
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함해 작성해 주세요.")
        if not any(char.isdigit() for char in password):
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함해 작성해 주세요.")
        if not any(char.isalpha() for char in password):
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함해 작성해 주세요.")
        return value
