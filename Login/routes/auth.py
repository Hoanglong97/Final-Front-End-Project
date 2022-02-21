from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from controller import users as user_controller
from models import schemas
from models.dbconfig import get_db
from utils import encrypt

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")


def get_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, encrypt.SECRET_KEY, algorithms=[encrypt.ALGORITHM])
    user_id: int = payload.get("sub")
    token_data = schemas.TokenData(user_id=user_id)
    return user_controller.get_user(token_data.user_id, db)


def authenticate_user(db: Session, username: str, password: str):
    user = user_controller.get_db_user(username, db)
    if not user:
        return False
    if not encrypt.verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=120)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, encrypt.SECRET_KEY, algorithm=encrypt.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, encrypt.SECRET_KEY, algorithms=encrypt.ALGORITHM)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = user_controller.get_user(token_data.user_id, db)
    if user is None:
        raise credentials_exception
    return user


@router.post('/token', response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=encrypt.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={'sub': str(user.id)}, expires_delta=access_token_expires
        )
        return schemas.Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get('/me', response_model=schemas.User)
async def read_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await get_current_user(token, db)
