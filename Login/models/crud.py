from datetime import datetime

from sqlalchemy.orm import Session

from utils import encrypt
from . import dbmodels, schemas


def get_user(db: Session, user_id: int):
    return db.query(dbmodels.User).filter(dbmodels.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    list_user = db.query(dbmodels.User).filter(dbmodels.User.username == username)
    return list_user.first()


def get_user_by_nickname(db: Session, nickname: str):
    return db.query(dbmodels.User).filter(dbmodels.User.nick_name == nickname).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(dbmodels.User).offset(skip).limit(limit).all()


# Get all user without limit number
def get_all_users(db: Session):
    return db.query(dbmodels.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    exist_user = get_user_by_username(db, user.username)
    if exist_user is not None:
        return None
    # hashed_pwd = encrypt.get_pwd_hashed(user.password)
    user_db = dbmodels.User(username=user.username,
                            hashed_password=user.password,
                            nick_name=user.nick_name,
                            date_of_birth=user.date_of_birth,
                            avatar=user.avatar
                            )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def login(db:Session,username: str ,password : str):
    exist_user = get_user_by_username(db,username)
    # hash_pwd = encrypt.get_pwd_hashed(password)
    if exist_user.hashed_password == password:
        return 1
    else:
        return 2


def update_user(db: Session, user: schemas.User, updated_user: schemas.UserUpdate):
    user.nick_name = updated_user.nick_name
    user.date_of_birth = updated_user.date_of_birth
    user.avatar = updated_user.avatar
    db.commit()
    db.refresh(user)
    return user


def update_user_nickname(db: Session, user: schemas.User, updated_user: schemas.UserUpdate):
    user.nick_name = updated_user.nick_name
    db.commit()
    db.refresh(user)
    return user


def update_user_avatar(db: Session, user: schemas.User, updated_user: schemas.UserUpdate):
    user.avatar = updated_user.avatar
    db.commit()
    db.refresh(user)
    return user


def update_user_birthday(db: Session, user: schemas.User, updated_user: schemas.UserUpdate):
    user.date_of_birth = updated_user.date_of_birth
    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, user: schemas.UserInDB, updated_user: schemas.UserUpdate):
    hashed_pwd = encrypt.get_pwd_hashed(updated_user.password)
    user.hashed_password = hashed_pwd
    db.commit()
    db.refresh(user)
    return user


def get_record(db: Session, record_id: int):
    return db.query(dbmodels.Record).filter(dbmodels.Record.id == record_id).first()


def get_records(db: Session, user: schemas.User):
    return db.query(dbmodels.Record).filter(dbmodels.Record.user_id == user.id)


def get_all_records_in_range(db: Session, user: schemas.User, start_date: datetime, end_date: datetime):
    return db.query(dbmodels.Record).filter(dbmodels.Record.record_date >= start_date,
                                            dbmodels.Record.record_date <= end_date,
                                            dbmodels.Record.user_id == user.id)


def get_record_by_day(db: Session, date_str: str, user: schemas.User):
    return db.query(dbmodels.Record).filter(dbmodels.Record.image == date_str,
                                            dbmodels.Record.user_id == user.id).first()


def get_records_by_day(db: Session, date_str: str):
    return db.query(dbmodels.Record).filter(dbmodels.Record.image == date_str).order_by(
        dbmodels.Record.distance.desc()).all()


def delete_record(db: Session, record: schemas.Record):
    db.delete(record)
    db.commit()
    return True


def update_record(db: Session, record: schemas.Record, point: int):
    record.point = point
    db.commit()
    db.refresh(record)
    return record


def create_record(db: Session, record: schemas.RecordCreate):
    db_record = dbmodels.Record(distance=record.distance,
                                duration=record.duration,
                                record_date=record.record_date,
                                image=record.image_path,
                                point=record.point,
                                update_count=record.update_count)
    if record.user_id is not None:
        user = get_user(db, record.user_id)
        db_record.user = user
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def add_record_to_user(db: Session, record_id: int, user_id: int):
    record = get_record(db, record_id)
    user = get_user(db, user_id)
    record.users.append(user)
    db.commit()
    db.refresh(record)
    return record


def get_ranking_day(db: Session, day_id: str):
    return db.query(dbmodels.Ranking_Day).filter(dbmodels.Ranking_Day.day_id == day_id).all()


def get_ranking_week(db: Session, week_id: str):
    return db.query(dbmodels.Ranking_Week).filter(dbmodels.Ranking_Week.week_id == week_id).all()


def get_ranking_month(db: Session, month_id: str):
    return db.query(dbmodels.Ranking_Month).filter(dbmodels.Ranking_Month.month_id == month_id).all()


def get_ranking_term(db: Session, term_id: str):
    return db.query(dbmodels.Ranking_Term).filter(dbmodels.Ranking_Term.term_id == term_id).all()


def get_ranking_year(db: Session, year_id: str):
    return db.query(dbmodels.Ranking_Year).filter(dbmodels.Ranking_Year.year_id == year_id).all()


def create_ranking_day(db: Session, day_id: str, user_id: int, rank: str, total_dis: float, total_dur: float,
                       total_point: int):
    db_ranking_day = dbmodels.Ranking_Day(day_id=day_id,
                                          rank=rank,
                                          total_distance=total_dis,
                                          total_duration=total_dur,
                                          total_point=total_point)
    if user_id is not None:
        user = get_user(db, user_id)
        db_ranking_day.user = user
    db.add(db_ranking_day)
    db.commit()
    db.refresh(db_ranking_day)
    return db_ranking_day


def create_ranking_week(db: Session, week_id: str, user_id: int, rank: str, total_dis: float, total_dur: int,
                        total_point: int):
    db_ranking_week = dbmodels.Ranking_Week(week_id=week_id,
                                            rank=rank,
                                            total_distance=total_dis,
                                            total_duration=total_dur,
                                            total_point=total_point)
    if user_id is not None:
        user = get_user(db, user_id)
        db_ranking_week.user = user
    db.add(db_ranking_week)
    db.commit()
    db.refresh(db_ranking_week)
    return db_ranking_week


def create_ranking_month(db: Session, month_id: str, user_id: int, rank: str, total_dis: float, total_dur: int,
                         total_point: int):
    db_ranking_month = dbmodels.Ranking_Month(month_id=month_id,
                                              rank=rank,
                                              total_distance=total_dis,
                                              total_duration=total_dur,
                                              total_point=total_point)
    if user_id is not None:
        user = get_user(db, user_id)
        db_ranking_month.user = user
    db.add(db_ranking_month)
    db.commit()
    db.refresh(db_ranking_month)
    return db_ranking_month


def create_ranking_term(db: Session, term_id: str, user_id: int, rank: str, total_dis: float, total_dur: int,
                        total_point: int):
    db_ranking_term = dbmodels.Ranking_Term(term_id=term_id,
                                            rank=rank,
                                            total_distance=total_dis,
                                            total_duration=total_dur,
                                            total_point=total_point)
    if user_id is not None:
        user = get_user(db, user_id)
        db_ranking_term.user = user
    db.add(db_ranking_term)
    db.commit()
    db.refresh(db_ranking_term)
    return db_ranking_term


def create_ranking_year(db: Session, year_id: str, user_id: int, rank: str, total_dis: float, total_dur: int,
                        total_point: int):
    db_ranking_year = dbmodels.Ranking_Year(year_id=year_id,
                                            rank=rank,
                                            total_distance=total_dis,
                                            total_duration=total_dur,
                                            total_point=total_point)
    if user_id is not None:
        user = get_user(db, user_id)
        db_ranking_year.user = user
    db.add(db_ranking_year)
    db.commit()
    db.refresh(db_ranking_year)
    return db_ranking_year


def update_ranking_day(db: Session, ranking_day: schemas.RankingDayUpdate, rank: str, total_dis: float,
                       total_dur: int, total_point: int):
    ranking_day.rank = rank
    ranking_day.total_distance = total_dis
    ranking_day.total_duration = total_dur
    ranking_day.total_point = total_point
    db.commit()
    db.refresh(ranking_day)
    return ranking_day


def update_ranking_week(db: Session, ranking_week: schemas.RankingWeekUpdate, rank: str, total_dis: float,
                        total_dur: int, total_point: int):
    ranking_week.rank = rank
    ranking_week.total_distance = total_dis
    ranking_week.total_duration = total_dur
    ranking_week.total_point = total_point
    db.commit()
    db.refresh(ranking_week)
    return ranking_week


def update_ranking_month(db: Session, ranking_month: schemas.RankingMonthUpdate, rank: str, total_dis: float,
                         total_dur: int, total_point: int):
    ranking_month.rank = rank
    ranking_month.total_duration = total_dur
    ranking_month.total_distance = total_dis
    ranking_month.total_point = total_point
    db.commit()
    db.refresh(ranking_month)
    return ranking_month


def update_ranking_term(db: Session, ranking_term: schemas.RankingTermUpdate, rank: str, total_dis: float,
                        total_dur: int, total_point: int):
    ranking_term.rank = rank
    ranking_term.total_duration = total_dur
    ranking_term.total_distance = total_dis
    ranking_term.total_point = total_point
    db.commit()
    db.refresh(ranking_term)
    return ranking_term


def update_ranking_year(db: Session, ranking_year: schemas.RankingYearUpdate, rank: str, total_dis: float,
                        total_dur: int, total_point: int):
    ranking_year.rank = rank
    ranking_year.total_distance = total_dis
    ranking_year.total_duration = total_dur
    ranking_year.total_point = total_point
    db.commit()
    db.refresh(ranking_year)
    return ranking_year


def create_notification(db: Session, notification: schemas.NotificationBase, user_id: int):
    db_notification = dbmodels.Notification(content_id=notification.content_id,
                                            content_type=notification.content_type,
                                            pre_rank=notification.pre_rank,
                                            cur_rank=notification.cur_rank,
                                            create_date=datetime.utcnow())
    if user_id is not None:
        user = get_user(db, user_id)
        db_notification.user = user
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_notifications(db: Session, user_id: int):
    return db.query(dbmodels.Notification).filter(dbmodels.Notification.user_id == user_id).all()


def get_notification_by_type(db: Session, user_id: int, date: str, date_type: str):
    return db.query(dbmodels.Notification).filter(dbmodels.Notification.user_id == user_id,
                                                  dbmodels.Notification.content_type == date_type,
                                                  dbmodels.Notification.content_id == date).all()


def get_notification_by_user(db: Session, user_id: int, date: str):
    return db.query(dbmodels.Notification).filter(dbmodels.Notification.user_id == user_id,
                                                  dbmodels.Notification.create_date.contains(date)).order_by(
        dbmodels.Notification.create_date.desc()).all()
