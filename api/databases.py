from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from motor.motor_asyncio import AsyncIOMotorClient


#--------------MariaDB----------------------------------
class DB_Settings(BaseSettings):
    DB_NAME : str
    DB_USER : str
    DB_PWD : str
    DB_HOST : str
    MONGO_URI : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    SECRET_KEY :str
    ALGORITHM :str
    model_config = SettingsConfigDict(env_file=".env")


db_settings = DB_Settings()

DATABASE_URL = f"mysql+pymysql://{db_settings.DB_USER}:{db_settings.DB_PWD}@{db_settings.DB_HOST}/{db_settings.DB_NAME}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()

#'-------------------------------------------------

#-----------------MONGO DB-------------------------
# class DB_Mongo_Settings(BaseSettings):
#     MONGO_URI : str
#     model_config = SettingsConfigDict(env_file=".env")

# mongo_conn = DB_Mongo_Settings()
# client = AsyncIOMotorClient(mongo_conn)

client = AsyncIOMotorClient(db_settings.MONGO_URI)

mongodb = client.lechucao_core
users = mongodb.users
et_plantilla = mongodb.ET_PLANTILLA
et_lc = mongodb.etlc
