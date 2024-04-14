"""
    file : App.API.Mydata_API.py
    writer : Meohong
    first date : 2024-04-14
    Objective : Mydata API ( Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-04-14 |   1   |   first write
    ========================================================================
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from typing_extensions import Annotated

from App.Service.Mydata_Service import MyDataService
from App.Service.user_Service import UserService
from App.api.user_API import oauth2_scheme
from App.database.repository import UserRepository
import pandas as pd

app = APIRouter(
    prefix="/Mydata",
)

user_service = Annotated[UserService, Depends()]
mydata_service = Annotated[MyDataService, Depends()]
user_repository = Annotated[UserRepository, Depends()]

@app.post("/getMonthsPayData")
async def get_months_Pay_data_from_csv(
        mydata_serv: mydata_service,
        user_serv: user_service,
        user_repo: user_repository,
        # login_token: Annotated[oauth2_scheme, Depends(oauth2_scheme)],
        csv_file: UploadFile = File(...),
):
    """
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Logined")
    """

    if csv_file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="csv_file is required")

    if csv_file.content_type == "text/csv":
        mydata_payinfo = mydata_serv.get_mydata_from_csv(csvfile=csv_file)
        print(mydata_payinfo)
        return HTTPException(status_code=status.HTTP_200_OK, detail="data read successfully")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="don't read")