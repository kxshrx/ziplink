from fastapi import Depends, HTTPException, Path, APIRouter
from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users, Urls
from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency  = Annotated[dict  , Depends(get_current_user)]

@router.get('/urls',status_code=status.HTTP_200_OK)
async def fetch_all_urls(user:user_dependency, db:db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(satus_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(Urls).all()

@router.delete('/ur;s/{short_code}', status_code=status.HTTP_200_OK)
async def delete_url(user:user_dependency, db:db_dependency, short_code:str):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(satus_code=status.HTTP_401_UNAUTHORIZED)
    rec_to_del = db.query(Urls).filter(Urls.short_code==short_code).first()
    if rec_to_del is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(Urls).filter(Urls.short_code==short_code).delete()
    db.commit()
    return 'url deleted successfully'


@router.get('/users', status_code=status.HTTP_200_OK)
async def fetch_all_urls(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(satus_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(Users).all()


@router.delete('/users/{userid}', status_code=status.HTTP_200_OK)
async def delete_url(user: user_dependency, db: db_dependency, userid: int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(satus_code=status.HTTP_401_UNAUTHORIZED)
    rec_to_del = db.query(Users).filter(Users.id == userid).first()
    if rec_to_del is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no such user')
    db.query(Urls).filter(Urls.owner_id==userid).delete()
    db.query(Users).filter(Users.id == userid).delete()
    db.commit()
    return 'user deleted successfully'

