import bcrypt
from fastapi import APIRouter, HTTPException, Request, Form, status
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..databases import SessionLocal
from passlib.hash import bcrypt
from ..crud import get_user


router=APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def compare_passwords(plain_pwd, stored_hash):
    is_match = bcrypt.verify(plain_pwd, stored_hash)
    return is_match


@router.post("/login",  response_class=HTMLResponse)
async def verify_password(request:Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    db  = SessionLocal()
    user = get_user(db, username=username)

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    is_match = compare_passwords(password, user.pwd)
    if is_match:
        return RedirectResponse(
            url="/home", 
            status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
        )