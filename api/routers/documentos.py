from typing import Annotated
from fastapi import FastAPI, APIRouter, HTTPException, status, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from ..databases import SessionLocal, Base, et_plantilla, mongodb
import api.crud as crud
from fastapi.templating import Jinja2Templates

from ..schemas import ET, Doc, doc_schema,docs_schema

router = APIRouter()


router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class ETRequest(BaseModel):
    et: str

@router.post("/documentos")
async def docs(request: Request, obra:Annotated[str,Form()]):
    
    try:
        if obra in await mongodb.list_collection_names():
            collection = mongodb[obra]
            docs_cursor = collection.find({})
            
            docs = await docs_cursor.to_list(length=None)
            # print (docs)
            data = await docs_schema(docs)

            return data
            # return templates.TemplateResponse(
            #     request=request,
            #     name="documentos.html",
            #     context={"documentos":data},
            # )
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})

    


