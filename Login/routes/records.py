from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi import File, UploadFile
from sqlalchemy.orm import Session

from controller import records as record_controller, ranking_trigger as ranking_controller, users as user_controller
from models import schemas
from models.dbconfig import get_db
from utils import env
from .auth import get_user_info

router = APIRouter()


@router.post('/upload', tags=["records"])
async def upload_record(distance: float = Form(...),
                        duration: int = Form(...),
                        record_date: str = Form(...),
                        image_file: UploadFile = File(...),
                        current_user: schemas.User = Depends(get_user_info),
                        db: Session = Depends(get_db)):
    datetime_object = datetime.strptime(record_date, "%Y-%m-%d %H:%M:%S")
    record = schemas.RecordCreate(distance=distance,
                                  duration=duration,
                                  user_id=current_user.id,
                                  record_date=datetime_object,
                                  point=0,
                                  update_count=0)

    result = record_controller.create_record(record, db, image_file, current_user)
    ranking_controller.ranking_day(db, datetime_object)
    ranking_controller.ranking_week(db, datetime_object)
    ranking_controller.ranking_month(db, datetime_object)
    ranking_controller.ranking_term(db, datetime_object)
    ranking_controller.ranking_year(db, datetime_object)
    return result


@router.get('/my_records', tags=["records"], response_model=List[schemas.Record])
async def my_records(current_user: schemas.User = Depends(get_user_info),
                     db: Session = Depends(get_db)):
    return record_controller.my_records(db, current_user)


@router.post('/get_records_by_user', tags=["records"], response_model=List[schemas.Record])
async def get_records_by_user(user_id: str = Form(...),
                              db: Session = Depends(get_db)):
    user = user_controller.get_user(int(user_id), db)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return record_controller.my_records(db, user)


@router.get('/my_records_in_range', tags=["records"], response_model=List[schemas.Record])
async def my_records_in_range(start_date: datetime,
                              end_date: datetime,
                              current_user: schemas.User = Depends(get_user_info),
                              db: Session = Depends(get_db)
                              ):
    return record_controller.get_all_records_in_range(db, current_user, start_date, end_date)


@router.post('/evidence_other_user', tags=["records"])
async def get_evidence(file_name: str = Form(...), user_id: str = Form(...), db: Session = Depends(get_db)):
    user = user_controller.get_user(int(user_id), db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    des = env.WORKING_PATH / 'records' / user.nick_name / file_name
    if des.exists():
        return '/resources/records/' + user.nick_name + '/' + file_name
    else:
        raise HTTPException(status_code=404, detail="File not found")


@router.post('/evidence_by_name', tags=["records"])
async def get_evidence(file_name: str = Form(...),
                       user: schemas.User = Depends(get_user_info)):
    des = env.WORKING_PATH / 'records' / user.nick_name / file_name
    if des.exists():
        return '/resources/records/' + user.nick_name + '/' + file_name
    else:
        raise HTTPException(status_code=404, detail="File not found")
