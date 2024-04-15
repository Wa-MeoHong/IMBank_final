"""
    file : App.API.Mydata_API.py
    writer : Meohong
    first date : 2024-04-14
    Objective : Mydata API ( Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-04-14 |   1   |   first write
     2024-04-15 |   2   |   account API write
    ========================================================================
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from typing_extensions import Annotated

from App.Service.Mydata_Service import MyDataService
from App.Service.user_Service import UserService
from App.api.user_API import oauth2_scheme
from App.database.repository import UserRepository, AccountRepository, MydataRepository
from App.Schema import Mydata_schema
import pandas as pd


app = APIRouter(
    prefix="/Mydata",
)

user_service = Annotated[UserService, Depends()]
mydata_service = Annotated[MyDataService, Depends()]
user_repository = Annotated[UserRepository, Depends()]
account_repository = Annotated[AccountRepository, Depends()]
mydata_repository = Annotated[MydataRepository, Depends()]

@app.get("/getAccount")
async def get_account(
        mydata_serv: mydata_service,
        user_serv: user_service,
        user_repo: user_repository,
        account_repo: account_repository,
        account_num: int,
        login_token: str = Depends(oauth2_scheme),

):
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Login")
    user_id = user_serv.get_user(email=user_email, user_repo=user_repo).id

    account = mydata_serv.get_account_info(user_id=user_id, account_num=account_num, account_repo=account_repo)
    return account if account is not None else HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

@app.post("/createAccount")
async def create_account(
        mydata_serv: mydata_service,
        user_serv: user_service,
        user_repo: user_repository,
        account_repo: account_repository,
        new_account: Mydata_schema.AccountForm = Depends(),
        login_token: str = Depends(oauth2_scheme),
):
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Login")
    user_id = user_serv.get_user(email=user_email, user_repo=user_repo).id

    account = mydata_serv.get_account_info(user_id=user_id, account_num=new_account.account_num, account_repo=account_repo)
    if account is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")

    account = mydata_serv.save_account_info(user_id=user_id, new_account=new_account, account_repo=account_repo)
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Account created")

@app.delete("/deleteAccount")
async def delete_account(
        mydata_serv: mydata_service,
        user_serv: user_service,
        user_repo: user_repository,
        account_repo: account_repository,
        account_num: int,
        login_token: str = Depends(oauth2_scheme),
):
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Login")
    user_id = user_serv.get_user(email=user_email, user_repo=user_repo).id

    account = mydata_serv.get_account_info(user_id=user_id, account_num=account_num, account_repo=account_repo)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="account Not Found")

    mydata_serv.delete_account_info(account_id=account.id, account_repo=account_repo)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Account deleted")

@app.post("/getMonthsPayData")
async def get_months_Pay_data_from_csv(
        mydata_serv: mydata_service,
        user_serv: user_service,
        user_repo: user_repository,
        login_token: Annotated[oauth2_scheme, Depends(oauth2_scheme)],
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