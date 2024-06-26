from fastapi import FastAPI, Request
from api.main import app
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request:Request):
    
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"name":"Diego"}

    )