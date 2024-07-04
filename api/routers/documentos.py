from typing import Annotated
from fastapi import FastAPI, APIRouter, HTTPException, status, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from passlib.hash import pbkdf2_sha256, bcrypt
from datetime import timedelta, timezone, datetime
from ..databases import SessionLocal, Base, et_plantilla, mongodb
import api.crud as crud
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..schemas import ET, Doc, doc_schema,docs_schema

import json

router = APIRouter()

# def get_db():
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class ETRequest(BaseModel):
    et: str



    
# Dependencia para obtener la sesión de la base de datos
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@router.post("/documentos", response_class=HTMLResponse)
async def docs(request: Request, obra:Annotated[str,Form()]):
    # et=et.et
    # data=[]
    # try:
    #     stmt = text(f"SELECT * FROM {obra} ")
    #     result = db.execute(statement=stmt)
    #     for res in result:
    #         et_dict = {
    #             "id": res[0],
    #             "codigo": res[1],
    #             "numero": res[2],
    #             "descripcion": res[3],
    #             "revision": res[4],
    #             "estado": res[5],
    #             "fecha_ingreso": res[6],
    #             "fecha_egreso": res[7],
    #             "N_informe": res[8],
    #             "NP": res[9],
    #             "file_url": res[10],
    #             "inf_url": res[11],
    #             "os": res[12],
    #             "OS_url": res[13],
    #         }
    #         data.append(et_dict)
    try:
        if obra in await mongodb.list_collection_names():
            collection = mongodb[obra]
            docs_cursor = collection.find({})
            
            docs = await docs_cursor.to_list(length=None)
            print (docs)
            data = await docs_schema(docs)

            
            return templates.TemplateResponse(
                request=request,
                name="documentos.html",
                context={"documentos":data},
            )
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})

    


