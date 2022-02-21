import shutil
from datetime import datetime

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from models import crud, schemas
from utils import env


def create_record(record: schemas.RecordCreate, db: Session, image_file: UploadFile, user: schemas.User):
    # Create folder for storing upload image
    des = env.WORKING_PATH / 'records' / user.username
    if not des.exists():
        des.mkdir(parents=True)
    today_str = record.record_date.strftime('%Y%m%d') + ".jpg"
    tmp_evidence = des / today_str
    # Write record information to database
    record.image_path = today_str
    record.update_count = 1
    record_in_day = crud.get_record_by_day(db, today_str, user)
    if record_in_day is not None:
        if record_in_day.update_count >= 3:
            raise HTTPException(status_code=405, detail="Reach Record Update Limit")
        record.update_count = record_in_day.update_count + 1
        crud.delete_record(db, record_in_day)
    record_db = crud.create_record(db, record)
    records_in_day = crud.get_records_by_day(db, today_str)

    for i in range(len(records_in_day)):
        if i == 0:
            crud.update_record(db, records_in_day[i], 10)
        elif i == 1:
            crud.update_record(db, records_in_day[i], 8)
        elif i == 2:
            crud.update_record(db, records_in_day[i], 6)
        elif i == 3:
            crud.update_record(db, records_in_day[i], 4)
        else:
            crud.update_record(db, records_in_day[i], 2)
    if record_db is None:
        raise HTTPException(status_code=405, detail="Cannot Create Record")

    # Upload image to storage folder
    with open(tmp_evidence, 'wb') as buffer:
        shutil.copyfileobj(image_file.file, buffer)

    # Return schemas Record after create successfully
    return schemas.Record(id=record_db.id,
                          distance=record_db.distance,
                          duration=record_db.duration,
                          image_path=record_db.image,
                          record_date=record_db.record_date,
                          create_at=record_db.create_date,
                          point=record_db.point,
                          update_count=record_db.update_count)


def my_records(db: Session, user: schemas.User):
    records = crud.get_records(db, user)
    return sorted(list(map(lambda db_record: schemas.Record(id=db_record.id,
                                                            distance=db_record.distance,
                                                            duration=db_record.duration,
                                                            record_date=db_record.record_date,
                                                            create_at=db_record.create_date,
                                                            update_count=db_record.update_count,
                                                            image_path='/resources/records/' + str(
                                                                user.nick_name) + '/' + db_record.image,
                                                            point=db_record.point),
                           records)), key=lambda record: record.record_date, reverse=True)


def get_all_records_in_range(db: Session, user: schemas.User, start_date: datetime, end_date: datetime):
    records = crud.get_all_records_in_range(db, user, start_date, end_date)
    return sorted(list(map(lambda db_record: schemas.Record(id=db_record.id,
                                                            distance=db_record.distance,
                                                            duration=db_record.duration,
                                                            record_date=db_record.record_date,
                                                            create_at=db_record.create_date,
                                                            image_path='/resources/records/' + str(
                                                                user.nick_name) + '/' + db_record.image,
                                                            point=db_record.point,
                                                            update_count=db_record.update_count),
                           records)), key=lambda record: record.record_date, reverse=True)
