"""
    file : App.Service.Mydata_Service.py
    writer : Meohong
    first date : 2024-03-24
    Objective : Mydata Service ( Actually Mydata Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-04-14 |   1   |   first write
     2024-04-15 |   2   |   account service write
    ========================================================================
"""
from http import HTTPStatus

from fastapi import HTTPException, status, File, UploadFile
import pandas as pd
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

    # 받은 CSV데이터를 가지고, DB에 저장하는 함수
    def save_mydata_from_csv(self, csvfile: UploadFile, account_id: int, mydata_repo: MydataRepository):
        # 받은 데이터를 데이터프레임으로 변환함
        df = pd.read_csv(csvfile.file)
        df["거래처"] = df["거래처"].str.strip()
        df = df[df["메모"] != "계좌 금액이동"].reset_index(drop=True)      # 계좌 금액이동은 제외해야함

        # 각 데이터프레임마다 하나씩 저장하는 과정을 거침
        for tuples in df.itertuples():
            # datetime 객체를 만들기위한 작업
            date_time_before = list(filter(None, re.split(r'[^0-9]', tuples.거래일시)))
            date_time = list(map(int, date_time_before))
            mydata_date = datetime(date_time[0], date_time[1], date_time[2]
                                   , date_time[3], date_time[4], date_time[5])

            mydata_date.strftime("%Y-%m-%d %H:%M:%S")
            # datetime 객체를 가지고, 먼저 데이터가 존재하는지 확인, 시간은 유일하기 때문에 가능한 일
            data = mydata_repo.get_datas_by_times(data_time=mydata_date.strftime("%Y-%m-%d %H:%M:%S"))
            if data is not None:
                continue

            # 데이터 생성
            mydata = Mydata.create(
                account_id=account_id,
                clients=tuples.거래처,
                dealcost=int(tuples.거래비용),
                leftcharge=int(tuples.남은금액),
                dealtime=mydata_date.strftime("%Y-%m-%d %H:%M:%S"),
                dealtype=tuples.메모
            )
            mydata_repo.save_mydata(mydata=mydata)
        return df

    def delete_mydata(self, account_id: int, mydata_repo: MydataRepository):
        mydata_repo.delete_mydata_by_account_id(account_id=account_id)
        return True

    def get_mydata(self, account_id: int, mydata_repo: MydataRepository):
        list_mydata = mydata_repo.get_datas_by_account_id(account_id=account_id)

        # 꺼낸 거래내역들을 딕셔너리화
        dict = {"거래처": [], "거래비용": [], "남은금액" : [], "거래일시": [], "메모": []}
        for mydata in list_mydata:
            dict["거래처"].append(mydata.clients)
            dict["거래비용"].append(mydata.dealcost)
            dict["남은금액"].append(mydata.leftcharge)
            dict["거래일시"].append(mydata.dealtime)
            dict["메모"].append(mydata.dealtype)

        # 딕셔너리 데이터를 데이터 프레임으로 만듦
        df = pd.DataFrame(dict)
        return df.to_dict("records")

    def get_mydata_by_months(self, data: dict, months: int):
        df = pd.DataFrame(data)
        latest = df["거래일시"][0]
        months_first = datetime(latest.year, latest.month, 1)
        months_ago = months_first - relativedelta(months=months)

        print(months_ago)

        df = df[df["거래일시"] >= months_ago]
        df["거래일시"] = df["거래일시"].dt.strftime("%Y-%m-%d %H:%M:%S")
        dict = df.to_dict(orient="list")
        return dict

    def analyze_data(self, data: dict):
        # 먼정 월별 데이터로 나눈 다음, 분석을 진행한다.
        df=pd.DataFrame(data)
        df["거래일시"] = pd.to_datetime(df["거래일시"])
        df["거래일시"] = df["거래일시"].dt.strftime("%Y-%m")
        print(df["거래일시"][0])

        groups = df.groupby("거래일시")
        print(groups)
        return

