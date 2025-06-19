import hashlib
import base64
from typing import Annotated
from starlette import status
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Urls
from routers.auth import get_current_user

router = APIRouter(
    prefix='/urls',
    tags=['urls']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency  = Annotated[dict  , Depends(get_current_user)]

now = datetime.now(timezone.utc)


class CreateRequestSchema(BaseModel):
    long_url:str

class CreatedReponseSchema(BaseModel):
    id:int
    url :str
    short_code : str
    created_at :datetime
    updated_at : datetime
    access_count : int

    class Config:
        orm_mode = True

class FetchShortResponseSchema(BaseModel):
    url:str
    class Config:
        orm_mode = True


def create_short_code(long_url: str, salt: str = '', length: int = 8) -> str:
    # Include salt in the hash to avoid collision
    input_str = long_url + salt
    hash_object = hashlib.sha256(input_str.encode())
    b64_encoded = base64.urlsafe_b64encode(hash_object.digest()).decode()
    return b64_encoded[:length]

def increment_access_count(short_code:str, db):
    url = db.query(Urls).filter(Urls.short_code==short_code).first()
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    url.access_count +=1
    db.commit()



@router.get('/', status_code=status.HTTP_200_OK)
async def see_all_urls(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='you are not an existing user')
    return db.query(Urls).filter(Urls.owner_id==user.get('id')).all()


@router.get('/{short_code}', response_model=FetchShortResponseSchema, status_code=status.HTTP_200_OK)
async def fetch_long_url(db:db_dependency, short_code:str):
    req_url = db.query(Urls).filter(Urls.short_code==short_code).first()
    if req_url is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    increment_access_count(short_code, db)
    return req_url

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CreatedReponseSchema)
async def shorten_url(user:user_dependency,db: db_dependency, urlreq: CreateRequestSchema):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='you are not an existing user')
    # Check if this long URL is already shortened
    existing_url = db.query(Urls).filter(Urls.url == urlreq.long_url).filter(Urls.owner_id==user.get('id')).first()
    if existing_url:
        return existing_url

    now = datetime.now(timezone.utc)
    short_url = create_short_code(urlreq.long_url)

    # Check if short_code already exists (rare, but possible collision)
    attempt = 1
    while db.query(Urls).filter(Urls.short_code == short_url).first():
        short_url = create_short_code(urlreq.long_url, salt=str(attempt))
        attempt += 1

    new_url = Urls(
        url=urlreq.long_url,
        short_code=short_url,
        access_count=0,
        created_at=now,
        updated_at=now,
        owner_id = user.get('id')
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return new_url


@router.delete('/{short_code}',status_code=status.HTTP_200_OK)
async def delete_record(user:user_dependency,db:db_dependency, short_code:str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='you are not an existing user')
    rec_to_delete = db.query(Urls).filter(Urls.short_code==short_code).filter(Urls.owner_id==user.get('id')).first()
    if rec_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such short URL found')

    db.query(Urls).filter(Urls.short_code==short_code).filter(Urls.owner_id==user.get('id')).delete()
    db.commit()
    return {'message':'deleted successfully'}



@router.put('/{short_code}',status_code = status.HTTP_200_OK)
async def update_record(user:user_dependency,db:db_dependency, short_code:str, updatereq:CreateRequestSchema):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='you are not an existing user')
    rec_to_update = db.query(Urls).filter(Urls.short_code==short_code).filter(Urls.owner_id==user.get('id')).first()
    if rec_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such short URL found')
    rec_to_update.url = updatereq.long_url
    rec_to_update.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(rec_to_update)

    return rec_to_update