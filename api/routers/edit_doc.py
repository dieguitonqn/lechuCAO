import os
import shutil
from typing import Union
from fastapi import APIRouter, status, Request, UploadFile, Depends, HTTPException
from fastapi.responses import HTMLResponse
from bson.objectid import ObjectId
from api.schemas import Doc
from api.databases import mongodb
from api.schemas import doc_schema
router = APIRouter()


@router.put("/update_doc", response_class=HTMLResponse())

async def updateDoc(request:Request, fileDoc:Union[UploadFile, None]=None): #UploadFile | None=None ):
    data = await request.form()
    obra = data.get("obra")
    print(fileDoc)
    if fileDoc.filename!='':


        carpeta = f"./DocumentosCAO/{obra}"
        path = os.path.join(carpeta, fileDoc.filename)

        doc = Doc(
            id=data.get("id"),
            codigo=data.get("codigo"),
            descripcion=data.get("descripcion"),
            revision=data.get("revision"),
            ultima_mod=data.get("ultima_mod"),
            link_doc=path,
        )
        doc_dict=dict(doc)

        print("Objeto doc: ",doc)
        
        del doc_dict["id"]
        print("Objeto dict: ",doc_dict)

        try:
            with open(path, "wb") as buffer:
                shutil.copyfileobj(fileDoc.file, buffer)
        except:
            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
        return HTMLResponse(status_code=status.HTTP_200_OK)
    else:
        print("No file uploaded.")
        doc = Doc(
            id=data.get("id"),
            codigo=data.get("codigo"),
            descripcion=data.get("descripcion"),
            revision=data.get("revision"),
            ultima_mod=data.get("ultima_mod"),
            link_doc=data.get("link_doc")
            )
        
        doc_dict=dict(doc)
        del doc_dict["id"]
        
        print("Objeto doc: ",doc)
        print("Objeto dict: ",doc_dict)
        collection = mongodb[data.get("obra")]
        try:
            await collection.find_one_and_replace({"_id":ObjectId(doc.id)}, doc_dict)
            return HTMLResponse(status_code=status.HTTP_201_CREATED)
        except:
            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
        
        

    



@router.post("/get_doc", response_model=Doc)
async def fet_doc(request:Request):
    data = await request.form()
    
    try:
        id = ObjectId(data.get("id"))
        collection = mongodb[data.get("obra")]
        data_db = await collection.find_one({"_id":id})
        return doc_schema(data_db)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)