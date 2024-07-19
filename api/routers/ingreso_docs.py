import shutil
from typing import List, Annotated
from fastapi import APIRouter, File, Form, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from api.databases import mongodb
from api.schemas import Doc
import os

router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@router.post("/ingreso_docs")
async def ingreso_docs( request:Request, fileDoc : List[UploadFile]):
    
    data = await request.form()
    obra = data.get ("obra")
    collection = mongodb[obra]
    carpeta = f"./{obra}"
    os.makedirs(carpeta, exist_ok=True)
    print (fileDoc)
    
    for i in range (1, int(data.get("numDocs"))+1):
        filecod = data.get(f"fileCod{i}")
        fileDesc = data.get(f"fileDesc{i}") 
        fileRev = data.get(f"fileRev{i}")
        fileDate = data.get (f"fileDate{i}")
        print(f"Archivo {i}: {fileDoc[i - 1].filename}, Código: {filecod}")
        print (filecod)
        print (fileDesc)
        print (fileRev)
        print (fileDate)
        print (fileDoc[i-1].filename)
        path = os.path.join(carpeta, fileDoc[i-1].filename)
        print(path)
        documentoInDB = Doc(descripcion=data.get(f"fileDesc{i}"),
                            codigo=data.get(f"fileCod{i}"),
                            revision=data.get(f"fileRev{i}"),
                            ultima_mod=data.get(f"fileDate{i}"),
                            link_doc= path)
        
        doc_dict = dict(documentoInDB)
        print(doc_dict)
        del doc_dict["id"]
        await collection.insert_one(doc_dict)


        with open(path, "wb") as buffer:
            shutil.copyfileobj(fileDoc[i-1].file, buffer)

    return HTMLResponse(status_code=status.HTTP_201_CREATED)
    # return RedirectResponse(
    #     url="http://10.222.48.245:3000/home", 
    #     status_code=status.HTTP_303_SEE_OTHER)
    
