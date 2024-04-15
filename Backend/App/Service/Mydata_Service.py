"""
    file : App.Service.Mydata_Service.py
    writer : Meohong
    first date : 2024-03-24
    Objective : Mydata Service ( Actually Mydata Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-04-14 |   1   |   first write

    ========================================================================
"""
from http import HTTPStatus

from fastapi import HTTPException, status, File, UploadFile
import pandas as pd
from passlib.context import CryptContext

from App.database.tables import Account, Mydata
from App.database.repository import AccountRepository, MydataRepository, UserRepository
from App.Schema.Mydata_schema import AccountForm

class MyDataService:
    def __init__(self):
        self.mydata = {}
        self.account_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def save_account_info(self, user_id: int, new_account: AccountForm, account_repo: AccountRepository):
        account = Account.create(
            user_id=user_id,
            account_num=str(new_account.account_num),
            objective=new_account.Objective,
        )
        account_repo.save_account(account=account)
        return account

    def delete_account_info(self, account_id: int, account_repo: AccountRepository):
        account_repo.delete_account(account_id=account_id)
        return True

    def get_account_info(self, user_id: int, account_num: int, account_repo: AccountRepository):
        account_list = account_repo.get_account_by_user_id(user_id=user_id)
        found_account = None
        # 계좌번호가 일치하는지 확인 후 계좌를 찾음
        for account in account_list:
            db_account_num = int(account.accountnum)
            if db_account_num == account_num:
                found_account = account
                break
        return found_account if found_account else None

    def get_mydata_from_csv(self, csvfile: UploadFile):
        df = pd.read_csv(csvfile.file)
        return df

