"""
    file : App.database.config.py
    writer : Meohong
    first date : 2024-02-21
    Objective : Configuration of Connecting to DB
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-02-21 |   1   |   first write
    ========================================================================
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

basedir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=basedir+'/.env')

class Settings(BaseSettings):
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_PORT: int = os.getenv("MYSQL_PORT")
    MYSQL_ROOT_PASSWORD: str = os.getenv("MYSQL_ROOT_PASSWORD")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE")

    class Config:
        env_file = '.env'
        extra = "ignore"

class JWTSettings(BaseSettings):
    JWT_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = '.env'
        extra = "ignore"

class WebUISetting(BaseSettings):
    WEBUI_URL: str = os.getenv("WEBUI_URL")
    WEBUI_STEPS: int = os.getenv("WEBUI_STEPS")
    POSITIVE_PROMPT: str = os.getenv("WEBUI_POSITIVE_PROMPT")
    NEGATIVE_PROMPT: str = os.getenv("WEBUI_NEGATIVE_PROMPT")
    SAVE_PATH: str = os.getenv("IMAGE_SAVE_PATH")

    class Config:
        env_file = '.env'
        extra = "ignore"
@lru_cache()
def jwt_setting():
    return JWTSettings()

@lru_cache()
def get_settings():
    return Settings()

@lru_cache()
def webui_setting():
    return WebUISetting()