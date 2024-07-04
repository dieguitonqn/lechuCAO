from fastapi import FastAPI, Request, APIRouter
from api.main import app
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.routers import documentos, mongo, login, ingreso_docs
from api.databases import mongodb

app = FastAPI()
app.include_router(documentos.router)
app.include_router(mongo.router)
app.include_router(login.router)
app.include_router(ingreso_docs.router)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"name":"Diego"}
    )

@app.get("/signin", response_class=HTMLResponse)
def siginin(request:Request):
    return(templates.TemplateResponse(
        request=request,
        name="signin.html",
        context={}
        )
    )

@app.get("/home", response_class=HTMLResponse)
async def home(request:Request):
    collections = await mongodb.list_collection_names()
    return (templates.TemplateResponse(
        request=request,
        name="home.html", 
        context={"collections" : collections}
        )
    )

@app.get("/docs_input", response_class=HTMLResponse)
async def docs_input(request:Request):
    collections = await mongodb.list_collection_names()
    return (templates.TemplateResponse(
        request=request,
        name="docs_input.html", 
        context={"collections" : collections}
        )
    )