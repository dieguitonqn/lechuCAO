from fastapi import FastAPI, Request, APIRouter
from api.main import app
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api import routers

app = FastAPI()
app.include_router(routers.router)
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
    return (templates.TemplateResponse(
        request=request,
        name="home.html"
    )

    )