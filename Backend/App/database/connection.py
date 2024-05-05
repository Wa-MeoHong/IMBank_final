"""
    file : App.database.connection.py
    writer : Meohong
    first date : 2024-02-21
    Objective : Connect to MySQL Database And Get_DB
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-02-21 |   1   |   first write

    ========================================================================
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from App.Security.config import get_settings

setting = get_settings()

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    'root',
    setting.MYSQL_ROOT_PASSWORD,
    setting.MYSQL_HOST,
    setting.MYSQL_PORT,
    setting.MYSQL_DATABASE,
)

db_engine = create_engine(SQLALCHEMY_DATABASE_URL,)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
