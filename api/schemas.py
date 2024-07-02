

from datetime import date
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


class ET(BaseModel):
    __tablename__ = None

    id :int
    codigo : str
    numero : str
    descripcion : str
    revision : str
    estado : str
    fecha_ingreso : str
    fecha_egreso : str
    N_informe : str
    NP : str
    file_url: str
    inf_url: str
    os : str
    OS_url : str



class UserBase(BaseModel):
    mail: str
    pwd: str
    nombre: str
    apellido: str
    rol: str
    obra: str
    enlinea: str
    lastlog: str
    

class UserInDB(UserBase):
    id: int
    pwdR: str
    class Config:
        orm_mode = True



class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls,v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectID')
        return str(v)

class ET(BaseModel):
    id: Optional[str] = Field(alias = ':id')
    codigo:str
    descripcion:str = None
    revision:str = None
    ultima_mod: date = None
    link_doc:str = None
    
    class Config:
        orm_mode =True
        allow_population_by_field_name = True
        json_encoders = {ObjectId:str}



def ets_schema (et) -> dict:
    return {
        
    }