from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from ..databases import et_plantilla
from bson import ObjectId
from ..schemas import doc_schema, Doc

router = APIRouter()



# @router.get("/docs_list", response_model=list(ET))
# async def mongodb():
#     return et_plantilla.find()

@router.post("/doc_input", response_model=Doc)
async def docinput(doc:Doc):
    if (await search_doc(doc.codigo)):
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="El documento ya existe")
    doc_dict = dict(doc)
    print(doc_dict)
    del doc_dict["id"]
    

    id = (await et_plantilla.insert_one(doc_dict)).inserted_id
    new_doc= await et_plantilla.find_one({"_id" : id})
    return doc_schema(new_doc)


async def search_doc(doc_cod:str) ->bool:
    try:
        doc = await et_plantilla.find_one({"codigo": doc_cod})
        return doc is not None
    except:
        return False
    