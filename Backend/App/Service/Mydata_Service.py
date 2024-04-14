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

from fastapi import HTTPException, status, File, UploadFile
import csv
import pandas as pd


class MyDataService:
    def __init__(self):
        self.mydata = {}

    def get_mydata_from_csv(self, csvfile: UploadFile):
        df = pd.read_csv(csvfile.file)
        return df

