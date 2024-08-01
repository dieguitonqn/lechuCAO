from typing import Annotated
from fastapi import Depends, FastAPI, Request, APIRouter
from fastapi.security import OAuth2PasswordBearer
from api.main import app
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from api.routers import documentos, mongo, login, ingreso_docs, pdfs, edit_doc
from api.databases import mongodb


app = FastAPI(openapi_prefix="/api")
app.include_router(documentos.router)
app.include_router(mongo.router)
app.include_router(login.router)
app.include_router(ingreso_docs.router)
app.include_router(pdfs.router)
app.include_router(edit_doc.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes ajustar esto según tus necesidades de seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/t_check")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# @app.get("/", response_class=HTMLResponse)
# def index(request:Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="index.html",
#         context={"name":"Diego"}
#     )

@app.get("/home")
async def home(request:Request, token:Annotated[str,Depends(oauth2)]):
    collections = await mongodb.list_collection_names()
    ordered_collections=sorted(collections)
    return ordered_collections

