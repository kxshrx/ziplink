from datetime import timedelta, timezone, datetime
from fastapi import HTTPException
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]



class CreateUserRequest(BaseModel):
    email:str
    username:str
    firstname:str
    lastname:str
    password:str
    role:str

class TokenResponse(BaseModel):
    access_token : str
    token_type:str



def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id:int, user_role:str, expires_delta:timedelta):
    encode = {'sub':username,'id':user_id,'user_role':user_role}
    expires = datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        userid: int = payload.get('id')
        user_role = payload.get('user_role')
        if userid is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
        return {'username':username, 'id': userid,'role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')




@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,userreq:CreateUserRequest):
    new_user = Users(
        email = userreq.email,
        username = userreq.username,
        firstname = userreq.firstname,
        lastname = userreq.lastname,
        hashed_password=bcrypt_context.hash(userreq.password),
        role = userreq.role,
        is_active = True
    )
    db.add(new_user)
    db.commit()


@router.post('/token', response_model=TokenResponse)
async def login_for_access_token(formdata: Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):
    user = authenticate_user(formdata.username, formdata.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
    token = create_access_token(user.username, user.id,user.role,timedelta(minutes=20) )
    return {'access_token':token, 'token_type':'bearer'}


