from typing import List

from fastapi import APIRouter, HTTPException, Form, File, UploadFile, Query
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from controller import users as user_controller
from models import schemas, crud
from models.dbconfig import get_db
from .auth import get_user_info

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")


@router.get("/{user_id}", tags=["users"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_controller.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", tags=["users"], response_model=schemas.User)
async def create_user(user: schemas.UserCreate,
                      db: Session = Depends(get_db)):
    return user_controller.create_user(user, db)

@router.post("/login",tags=["users"])
async def login(user:schemas.Login,
                db: Session = Depends(get_db)):
    return user_controller.login(user,db)

@router.get("/", tags=["users"], response_model=List[schemas.User])
async def get_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return user_controller.get_users(skip, limit, db)


@router.put("/update_info", tags=["users"])
async def update_info(nick_name: str = Form(...),
                      date_of_birth: str = Form(...),
                      avatar: UploadFile = File(...),
                      current_user: schemas.User = Depends(get_user_info),
                      db: Session = Depends(get_db)):
    return user_controller.updated_user(current_user, db, nick_name, date_of_birth, avatar)


@router.post("/update_nickname", tags=["users"])
async def update_nickname(nick_name: str = Form(...),
                          current_user: schemas.User = Depends(get_user_info),
                          db: Session = Depends(get_db)):
    return user_controller.updated_user_nickname(current_user, db, nick_name)


@router.post("/update_avatar", tags=["users"])
async def update_avatar(avatar: UploadFile = File(...),
                        current_user: schemas.User = Depends(get_user_info),
                        db: Session = Depends(get_db)):
    return user_controller.updated_user_avatar(current_user, db, avatar)


@router.post("/update_birthday", tags=["users"])
async def update_birthday(date_of_birth: str = Form(...),
                          current_user: schemas.User = Depends(get_user_info),
                          db: Session = Depends(get_db)):
    return user_controller.updated_user_birthday(current_user, db, date_of_birth)


@router.post("/update_password", tags=["users"])
async def update_password(new_password: str = Form(...),
                          current_user: schemas.User = Depends(get_user_info),
                          db: Session = Depends(get_db)):
    return user_controller.updated_user_password(current_user, db, new_password)


@router.post("/overview_user", tags=["users"], response_model=schemas.OverviewUser)
async def get_overview_user(current_user: schemas.User = Depends(get_user_info),
                            db: Session = Depends(get_db)):
    return user_controller.get_overview_user(db, current_user)


@router.post("/overview_user_by_nickname", tags=["users"], response_model=schemas.OverviewUser)
async def get_overview_user_by_nickname(nick_name: str = Form(...),
                                        db: Session = Depends(get_db)):
    user = crud.get_user_by_nickname(db, nick_name)
    if user is not None:
        return user_controller.get_overview_user(db, user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/overview", tags=["users"], response_model=schemas.Overview)
async def get_overview_by_type(date_type=Query("Day", enum=["Day", "Week", "Month", "Year", "Term"]),
                               db: Session = Depends(get_db)):
    return user_controller.get_overview_by_type(db, date_type)


@router.post("/avatar", tags=["users"])
async def get_avatar(user: schemas.User = Depends(get_user_info)):
    des = '/resources/users/' + user.avatar
    return des
