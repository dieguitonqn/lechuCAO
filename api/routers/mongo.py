from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..databases import et_plantilla
from bson import ObjectId
from ..schemas import ET

router = APIRouter()



@router.get("/docs_list", response_model=list(ET))
async def mongodb():
    return et_plantilla.find()

@router.post("/doc_input")
async def docinput(et:ET):
    et_dict = dict(et)
    et_plantilla.insert_one(et_dict)