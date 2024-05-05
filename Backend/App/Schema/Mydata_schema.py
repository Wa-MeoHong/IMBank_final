from pydantic import BaseModel, field_validator, SecretStr
from fastapi import HTTPException, status

class AccountForm(BaseModel):
    account_num: int
    Objective: str

    # 유효성 검사 진행
    @field_validator('Objective')
    def check_account_empty(cls, value):
        if not value or value.isspace():
            raise HTTPException(status_code=422, detail='거래 목적을 입력 하세요')
        return value
    @field_validator('account_num')
    def check_account_num(cls, value):
        if value is None:
            raise HTTPException(status_code=422, detail="계좌 번호를 입력 하세요")
        return value