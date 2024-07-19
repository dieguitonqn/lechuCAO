from datetime import timedelta, datetime, timezone
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import jwt
from pydantic import BaseModel
from ..databases import SessionLocal, db_settings
from passlib.hash import bcrypt
from ..crud import get_user


router=APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

def compare_passwords(plain_pwd, stored_hash):
    is_match = bcrypt.verify(plain_pwd, stored_hash)
    return is_match

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})
    print (to_encode)
    encoded_jwt = jwt.encode(to_encode, db_settings.SECRET_KEY, algorithm=db_settings.ALGORITHM)
    return encoded_jwt

class Token(BaseModel):
    token: str
    token_type : str

class LoginForm(BaseModel):
    username : str
    password : str

@router.post("/login",  response_model= Token)
async def verify_password(request:Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
# async def verify_password(request:Request, formData : LoginForm=Form(...)):
    db  = SessionLocal()
    user = get_user(db, username=username)

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    is_match = compare_passwords(password, user.pwd)
    
    if is_match:
        token_exp = timedelta(minutes=db_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(data={'sub' : user.mail, 'rol':user.rol}, expires_delta=token_exp)
        print (token)
        return Token(token=token, token_type ="bearer")
    else:
        raise HTTPException(status_code=401, detail="Password Incorrecto")
            # return RedirectResponse(
            #     url="10.222.48.245:3000/login", 
            #     status_code=status.HTTP_303_SEE_OTHER)
    # else:
    #     return templates.TemplateResponse(
    #         request=request,
    #         name="index.html",
    #     )
    

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/t_check")
async def verify_token(token: Annotated[str, Depends(oauth2)]):
    try:
        payload = jwt.decode(token, db_settings.SECRET_KEY, algorithms=[db_settings.ALGORITHM])
        # Check if token has expired
        current_time = datetime.now(timezone.utc)
        print(payload.get("exp"))
        print(current_time.timestamp())
        if payload.get("exp") < current_time.timestamp():
            print(True)
        else:
            print(False)


        # if payload.get("exp") is None or payload.get("exp") < current_time.timestamp():
        #     print(True)
        #     raise HTTPException(status_code=401, detail="Token has expired")
        # Token is valid, return a success message (optional)
        token = create_access_token(data={'sub':payload.get("sub"), 'rol':payload.get('rol')}, expires_delta=timedelta(minutes=1))
        return {"message": "Token is valid", "token":token}

    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    
@router.get('/t_admin_check')
async def check_admin(token:Annotated[str, Depends(oauth2)]):
    try:
        payload = jwt.decode(token, db_settings.SECRET_KEY, algorithms=[db_settings.ALGORITHM])
        print ( payload.get("rol"))
        if payload.get("rol") in ["admin", "autorizado"]:
            return HTMLResponse(status_code=status.HTTP_202_ACCEPTED)
        else:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)