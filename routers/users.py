from fastapi import Depends, HTTPException, Path, APIRouter
from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users
from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix='/users',
    tags=['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency  = Annotated[dict  , Depends(get_current_user)]


class UserResponseModel(BaseModel):
    id:int
    firstname :str
    lastname:str
    username:str
    role:str

class UserVerification(BaseModel):
    password:str
    new_password : str =Field(min_length=6)

@router.get('/', response_model=UserResponseModel, status_code=status.HTTP_200_OK)
async def user_details(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = user.get('id')
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_details = db.query(Users).filter(Users.id == user_id).first()
    return {
        'id':user_details.id,
        'firstname':user_details.firstname,
        'lastname':user_details.lastname,
        'username': user_details.username,
        'role': user_details.role
    }

@router.put('/password', status_code=status.HTTP_200_OK)
async def update_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_to_update = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not bcrypt_context.verify(user_verification.password, user_to_update.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    user_to_update.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_to_update)
    db.commit()
    db.refresh(user_to_update)

    return {'message': 'Password updated successfully'}
