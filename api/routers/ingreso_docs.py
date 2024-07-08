from typing import List, Annotated
from fastapi import APIRouter, File, Form, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from api.databases import mongodb
from api.models import FormDataRow

router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class FormDataModel(BaseModel):
    data: List[FormDataRow]

class Obra(BaseModel):
    obra:str



class FormField(BaseModel):
    name: str = Field(...)
    value: str = Field(...)
    file: UploadFile = Field(None)  # Add file field

class FormSchema(BaseModel):
    fields: List[FormField] = Field(...)


@router.post("/ingreso_docs")
async def ingreso_docs( request:Request, fileDoc : List[UploadFile]):
    # obra: str = Form(...),  # Campo de texto
    # # numDocs: int = Form(...),  # Campo de texto para la cantidad de documentos
    # files: List[UploadFile] = File(...),  # Lista de archivos
    # fileCod: List[str] = Form(...),  # Lista de códigos de documentos
    # fileDesc: List[str] = Form(...),  # Lista de descripciones de documentos
    # fileRev: List[str] = Form(...),  # Lista de revisiones de documentos
# ):
    
    # # Procesar los datos recibidos
    # for idx, file in enumerate(files):
    #     contents = await file.read()
    #     print(f"Archivo {idx + 1}: {file.filename}, tamaño: {len(contents)} bytes")

    # # Iterar sobre las listas de campos de texto
    # for i in range(len(fileCod)):
    #     print(f"Documento {i + 1}: Código={fileCod[i]}, Descripción={fileDesc[i]}, Revisión={fileRev[i]}")

    # # Puedes hacer lo que necesites con los datos aquí, como guardarlos en una base de datos
    data = await request.form()
    print (data)
    print(data.get("numDocs"))

    print({"filenames": [file.filename for file in fileDoc]})
    return {"message": "Formulario recibido exitosamente"}
    # return RedirectResponse(
    #         url="/home", 
    #         status_code=status.HTTP_303_SEE_OTHER)