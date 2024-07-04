from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.databases import mongodb


router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

