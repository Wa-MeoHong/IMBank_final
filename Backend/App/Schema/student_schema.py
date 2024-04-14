from pydantic import BaseModel, PastDate, field_validator
from fastapi import HTTPException, status

class StudentForm(BaseModel):
    student_id: int
    university_name: str
    major: str


    # 필드가 비어있는지, 확인하는 곳
    @field_validator( "university_name","major")
    def check_empty(cls, value):
        if not value or value.isspace():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="필수 항목을 입력 하세오.")
        return value

    @field_validator("student_id")
    def check_id(cls, value):
        if isinstance(value, int):
           return value
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="학번을 입력해 주세요")
