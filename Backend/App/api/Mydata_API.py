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

from fastapi.responses import JSONResponse
from App.Service.Mydata_Service import MyDataService
from App.Service.user_Service import UserService
from App.api.user_API import oauth2_scheme
from App.database.repository import UserRepository, AccountRepository, MydataRepository
from App.Schema import Mydata_schema

app = APIRouter(
    prefix="/Mydata",
)

user_service = Annotated[UserService, Depends()]
mydata_service = Annotated[MyDataService, Depends()]
user_repository = Annotated[UserRepository, Depends()]
mydata_repository = Annotated[MydataRepository, Depends()]
account_repository = Annotated[AccountRepository, Depends()]

@app.post("/getAccount")
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

@app.post("/saveMonthsPayData")
async def get_months_Pay_data_from_csv(
        mydata_serv: mydata_service,
        user_serv: user_service,
        user_repo: user_repository,
        mydata_repo: mydata_repository,
        account_repo: account_repository,
        login_token: Annotated[oauth2_scheme, Depends(oauth2_scheme)],
        account_num: int,
        csv_file: UploadFile = File(...),
):
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Logined")
    # 계좌정보를 들고 옴
    user_id = user_serv.get_user(email=user_email, user_repo=user_repo).id
    account = mydata_serv.get_account_info(user_id=user_id, account_num=account_num, account_repo=account_repo)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="account Not Found")

    # 파일이 입력되어 있는지 확인
    if csv_file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="csv_file is required")

    # 파일이 CSV파일임을 확인하고 작업을 진행
    if csv_file.content_type == "text/csv":
        mydata_payinfo = mydata_serv.save_mydata_from_csv(account_id=account.id, csvfile=csv_file,
                                                          mydata_repo=mydata_repo)
        return HTTPException(status_code=status.HTTP_200_OK, detail="data read successfully")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="don't read")

@app.delete("/deleteMonthsPayData")
async def delete_PayData_account_num(
        mydata_serv: mydata_service,
        user_serv: user_service,
        user_repo: user_repository,
        mydata_repo: mydata_repository,
        account_repo: account_repository,
        login_token: Annotated[oauth2_scheme, Depends(oauth2_scheme)],
        account_num: int,
):
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Logined")
    # 계좌정보를 들고 옴
    user_id = user_serv.get_user(email=user_email, user_repo=user_repo).id
    account = mydata_serv.get_account_info(user_id=user_id, account_num=account_num, account_repo=account_repo)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="account Not Found")

    # 계좌번호내에 있는 모든 데이터를 지운다
    mydata_serv.delete_mydata(account_id=account.id, mydata_repo=mydata_repo)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Datas deleted")

@app.get("/getMonthsData")
async def get_months_pay_data_for_Months(
        mydata_serv: mydata_service,
        user_serv: user_service,
        user_repo: user_repository,
        mydata_repo: mydata_repository,
        account_repo: account_repository,
        login_token: Annotated[oauth2_scheme, Depends(oauth2_scheme)],
        account_num: int,
        before_months: int = 1,
):
    try:
        user_email = user_serv.decode_access_token(access_token=login_token)
        if user_email is None:
            raise
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Logined")
    # 계좌정보를 들고 옴
    user_id = user_serv.get_user(email=user_email, user_repo=user_repo).id
    account = mydata_serv.get_account_info(user_id=user_id, account_num=account_num, account_repo=account_repo)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="account Not Found")

    # 월별 데이터를 가져옴
    df_for_dict = mydata_serv.get_mydata(account_id=account.id, mydata_repo=mydata_repo)
    df_result = mydata_serv.get_mydata_by_months(data=df_for_dict, months=before_months)
    return JSONResponse(content=df_result)

@app.post("/analyzedata")
async def analyze_data(
        mydata_serv: mydata_service,
        user_serv: user_service,
        user_repo: user_repository,
        mydata_repo: mydata_repository,
        account_repo: account_repository,
        login_token: Annotated[oauth2_scheme, Depends(oauth2_scheme)],
        data : dict,
):
    mydata_serv.analyze_data(data=data)
    return data
