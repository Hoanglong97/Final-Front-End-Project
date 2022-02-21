import os
import shutil
from calendar import monthrange
from datetime import datetime, date, timedelta

import magic
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from controller import ranking as ranking_controller
from models import crud
from models import schemas
from utils import env, utils


def get_user(user_id: int, db: Session):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        return None
    user = schemas.User(id=db_user.id,
                        username=db_user.username,
                        nick_name=db_user.nick_name,
                        date_of_birth=db_user.date_of_birth,
                        create_at=db_user.create_date,
                        avatar=db_user.avatar)
    return user


def get_users(skip: int, limit: int, db: Session):
    users = crud.get_users(db, skip, limit)
    return list(map(lambda db_user: schemas.User(id=db_user.id,
                                                 username=db_user.username,
                                                 nick_name=db_user.nick_name,
                                                 date_of_birth=db_user.date_of_birth,
                                                 create_at=db_user.create_date,
                                                 avatar=db_user.avatar),
                    users))


# Get all user without limit number
def get_all_users(db: Session):
    users = crud.get_all_users(db)
    return list(map(lambda db_user: schemas.User(id=db_user.id,
                                                 username=db_user.username,
                                                 nick_name=db_user.nick_name,
                                                 date_of_birth=db_user.date_of_birth,
                                                 create_at=db_user.create_date,
                                                 avatar=db_user.avatar),
                    users))


def create_user(user: schemas.UserCreate, db: Session):
    user.avatar = "default.jpg"
    db_user = crud.create_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=409, detail="User already registered")

    return schemas.User(id=db_user.id,
                        username=db_user.username,
                        nick_name=db_user.nick_name,
                        date_of_birth=db_user.date_of_birth,
                        create_at=db_user.create_date,
                        avatar=db_user.avatar)

def login(user: schemas.Login,db: Session):
    user_exist = crud.get_user_by_username(db, user.username)
    if not user_exist:
        return False
    user_login = crud.login(db,user.username,user.password)
    if user_login == 1:
        return True
    else:
        return False

def get_db_user(username: str, db: Session):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return schemas.UserInDB(id=user.id,
                            username=user.username,
                            nick_name=user.nick_name,
                            hashed_password=user.hashed_password,
                            create_at=user.create_date,
                            avatar=user.avatar)


def updated_user(user: schemas.User, db: Session, nick_name, date_of_birth, avatar: UploadFile):
    user_in_db = crud.get_user(db, user.id)
    des = env.WORKING_PATH / 'users'
    if avatar.content_type.__contains__("image"):
        if not des.exists():
            des.mkdir(parents=True)
        update_user = schemas.UserUpdate(nick_name=nick_name,
                                         date_of_birth=date_of_birth,
                                         avatar=avatar.filename
                                         )
        tmp_evidence = des / avatar.filename
        with open(tmp_evidence, 'wb') as buffer:
            shutil.copyfileobj(avatar.file, buffer)
        result = crud.update_user(db, user_in_db, update_user)
        if result:
            return result
        else:
            return schemas.Result(result="Error", error="Can not update user")
    else:
        return schemas.Result(result="Error", error="Avatar should be image")


def updated_user_nickname(user: schemas.User, db: Session, nick_name):
    user_in_db = crud.get_user(db, user.id)
    user = crud.get_user_by_nickname(db,nick_name)
    if user is not None:
        raise HTTPException(status_code=409, detail="User already existed")
    update_user = schemas.UserUpdate(nick_name=nick_name)
    result = crud.update_user_nickname(db, user_in_db, update_user)
    if result:
        return result
    else:
        return schemas.Result(result="Error", error="Can not update user")


def updated_user_avatar(user: schemas.User, db: Session, avatar: UploadFile):
    user_in_db = crud.get_user(db, user.id)
    des = env.WORKING_PATH / 'users'
    if not des.exists():
        des.mkdir(parents=True)
    today_str = user.nick_name + os.path.splitext(avatar.filename)[1]
    tmp_evidence = des / today_str
    update_user = schemas.UserUpdate(avatar=today_str)
    try:
        with open(tmp_evidence, 'wb') as buffer:
            shutil.copyfileobj(avatar.file, buffer)
    except shutil.Error:
        raise HTTPException(status_code=404, detail="Cannot copy file to server")
    if 'image' not in (magic.from_file(str(tmp_evidence), mime=True)):
        raise HTTPException(status_code=404, detail="Avatar should be image")
    else:
        result = crud.update_user_avatar(db, user_in_db, update_user)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Can not update user")


def updated_user_birthday(user: schemas.User, db: Session, date_of_birth):
    user_in_db = crud.get_user(db, user.id)
    update_user = schemas.UserUpdate(date_of_birth=date_of_birth)
    result = crud.update_user_birthday(db, user_in_db, update_user)
    if result:
        return result
    else:
        return schemas.Result(result="Error", error="Can not update user")


def updated_user_password(user: schemas.User, db: Session, new_password):
    user_in_db = crud.get_user(db, user.id)
    update_user = schemas.UserUpdate(password=new_password)
    result = crud.update_user_password(db, user_in_db, update_user)
    if result:
        return result
    else:
        return schemas.Result(result="Error", error="Can not update user")


def get_overview_user(db: Session, current_user: schemas.User):
    datetime_now = datetime.utcnow()
    start_day = datetime_now.replace(hour=00).replace(minute=00).replace(second=00)
    end_day = datetime_now.replace(hour=23).replace(minute=59).replace(second=00)
    start_week, end_week = utils.get_day_of_week(datetime_now)
    start_month = datetime_now.replace(day=1)
    end_month = datetime_now.replace(day=monthrange(datetime_now.year, datetime_now.month)[1])
    start_year = date(datetime_now.year, 1, 1)
    end_year = date(datetime_now.year, 12, 31)
    day_list = ranking_controller.ranking_in_range(db, start_day, end_day)
    week_list = ranking_controller.ranking_in_range(db, start_week, end_week)
    month_list = ranking_controller.ranking_in_range(db, start_month, end_month)
    year_list = ranking_controller.ranking_in_range(db, start_year, end_year)
    distance, duration, _ = ranking_controller.total_score(day_list, current_user)
    week, _, _ = ranking_controller.total_score(week_list, current_user)
    month, _, _ = ranking_controller.total_score(month_list, current_user)
    year, _, _ = ranking_controller.total_score(year_list, current_user)
    overview = schemas.OverviewUser(
        nick_name=current_user.nick_name,
        distance=distance,
        duration=duration,
        week=week,
        month=month,
        year=year)
    return overview


def get_overview_by_type(db: Session, date_type: str):
    datetime_now = datetime.utcnow()
    distance = duration = 0
    dis_change = dur_change = True
    if date_type == "Day":
        day_id = datetime_now.strftime("%Y%m%d")
        distance, duration = get_total(crud.get_ranking_day(db, day_id))
        pre_day_id = (datetime_now - timedelta(days=1)).strftime("%Y%m%d")
        pre_dis, pre_dur = get_total(crud.get_ranking_day(db, pre_day_id))
        if distance < pre_dis:
            dis_change = False
        if duration < pre_dur:
            dur_change = False
    if date_type == "Week":
        start_week, end_week = utils.get_day_of_week(datetime_now)
        week_id = start_week.strftime("%Y%m%d") + '_' + end_week.strftime("%Y%m%d")
        distance, duration = get_total(crud.get_ranking_week(db, week_id))
        pre_start_week, pre_end_week = utils.get_day_of_week(start_week.replace(day=start_week.day - 1))
        pre_week_id = pre_start_week.strftime("%Y%m%d") + '_' + pre_end_week.strftime("%Y%m%d")
        pre_dis, pre_dur = get_total(crud.get_ranking_week(db, pre_week_id))
        if distance < pre_dis:
            dis_change = False
        if duration < pre_dur:
            dur_change = False
    if date_type == "Month":
        month_id = datetime_now.strftime("%Y%m")
        distance, duration = get_total(crud.get_ranking_month(db, month_id))
        if datetime_now.month == 1:
            pre_month_id = (datetime_now.replace(month=12).replace(year=datetime_now.year - 1)).strftime("%Y%m")
            pre_month_list = crud.get_ranking_month(db, pre_month_id)
        else:
            pre_month_id = (datetime_now.replace(month=datetime_now.month - 1)).strftime("%Y%m")
            pre_month_list = crud.get_ranking_month(db, pre_month_id)
        pre_dis, pre_dur = get_total(pre_month_list)
        if distance < pre_dis:
            dis_change = False
        if duration < pre_dur:
            dur_change = False
    if date_type == "Year":
        year_id = datetime_now.strftime("%Y")
        distance, duration = get_total(crud.get_ranking_year(db, year_id))
        pre_year_id = (datetime_now.replace(year=datetime_now.year - 1)).strftime("%Y")
        pre_dis, pre_dur = get_total(crud.get_ranking_year(db, pre_year_id))
        if distance < pre_dis:
            dis_change = False
        if duration < pre_dur:
            dur_change = False
    if date_type == "Term":
        start_term, end_term = utils.get_day_of_term(datetime_now)
        term_id = start_term.strftime("%Y%m") + "_" + end_term.strftime("%Y%m")
        distance, duration = get_total(crud.get_ranking_term(db, term_id))
        pre_start_term, pre_end_term = utils.get_day_of_term(start_term.replace(month=start_term.month - 1))
        pre_term_id = pre_start_term.strftime("%Y%m") + "_" + pre_end_term.strftime("%Y%m")
        pre_dis, pre_dur = get_total(crud.get_ranking_term(db, pre_term_id))
        if distance < pre_dis:
            dis_change = False
        if duration < pre_dur:
            dur_change = False
    overview = schemas.Overview(
        distance=distance,
        dis_change=dis_change,
        duration=duration,
        dur_change=dur_change
    )
    return overview


def get_total(list_elements):
    dis = dur = 0
    if list_elements:
        for i in range(len(list_elements)):
            dis = dis + list_elements[i].total_distance
            dur = dur + list_elements[i].total_duration
        return dis, dur
    else:
        return dis, dur
