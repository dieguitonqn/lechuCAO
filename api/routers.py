from typing import Annotated
from fastapi import FastAPI, APIRouter, HTTPException, status, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from passlib.hash import pbkdf2_sha256, bcrypt
from datetime import timedelta, timezone, datetime
from .databases import SessionLocal, Base
import api.crud as crud
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from .schemas import ET

import json

router = APIRouter()

# def get_db():
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

def compare_passwords(plain_pwd, stored_hash):
    is_match = bcrypt.verify(plain_pwd, stored_hash)
    return is_match


class ETRequest(BaseModel):
    et: str




router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@router.post("/login",  response_class=HTMLResponse)
async def verify_password(request:Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    db  = SessionLocal()
    user = crud.get_user(db, username=username)

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    is_match = compare_passwords(password, user.pwd)
    if is_match:
        return RedirectResponse(
            url="/home", 
            status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
        )
    
# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/documentos", response_class=HTMLResponse)
async def docs(request: Request, obra:Annotated[str,Form()], db: Session = Depends(get_db)):
    # et=et.et
    data=[]
    try:
        stmt = text(f"SELECT * FROM {obra} where estado ='CAO'")
        result = db.execute(statement=stmt)
        for res in result:
            et_dict = {
                "id": res[0],
                "codigo": res[1],
                "numero": res[2],
                "descripcion": res[3],
                "revision": res[4],
                "estado": res[5],
                "fecha_ingreso": res[6],
                "fecha_egreso": res[7],
                "N_informe": res[8],
                "NP": res[9],
                "file_url": res[10],
                "inf_url": res[11],
                "os": res[12],
                "OS_url": res[13],
            }
            data.append(et_dict)



        return templates.TemplateResponse(
            request=request,
            name="documentos.html",
            context={"documentos":data},
        )
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})
    finally:
        db.close()
    
