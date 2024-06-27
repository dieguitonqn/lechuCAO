from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

class DB_Settings(BaseSettings):
    DB_NAME : str
    DB_USER : str
    DB_PWD : str
    DB_HOST : str
    model_config = SettingsConfigDict(env_file=".env")


db_settings = DB_Settings()

DATABASE_URL = f"mysql+pymysql://{db_settings.DB_USER}:{db_settings.DB_PWD}@{db_settings.DB_HOST}/{db_settings.DB_NAME}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()