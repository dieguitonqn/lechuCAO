

from datetime import date
from bson.objectid import ObjectId
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


class Doc(BaseModel):
    id: Optional[str] = Field(default=None, description="MongoDB OjectID")
    codigo:str
    descripcion:str = None
    revision:str = None
    ultima_mod: str = None
    link_doc:str = None
    


def doc_schema (doc) -> dict:
    return {
        "id" : str(doc['_id']),
        "codigo" : doc["codigo"],
        "descripcion" : doc["descripcion"],
        "revision" : doc["revision"],
        "ultima_mod" : doc["ultima_mod"], 
        "link_doc" : doc["link_doc"]
    }

async def docs_schema (docs:dict)-> list:
    return [doc_schema(doc) for doc in docs]