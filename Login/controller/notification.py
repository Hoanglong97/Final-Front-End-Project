from datetime import datetime, date

from sqlalchemy.orm import Session

from models import crud
from models import schemas
from utils import utils


def get_notifications(user_id: int, db: Session):
    notification = crud.get_notifications(db, user_id)
    return list(map(lambda db_notification: schemas.NotificationBase(content_id=db_notification.content_id,
                                                                     content_type=db_notification.content_type,
                                                                     pre_rank=db_notification.pre_rank,
                                                                     cur_rank=db_notification.cur_rank,
                                                                     create_date=db_notification.create_date,
                                                                     user_id=db_notification.user_id),
                    notification))


def get_notifications_in_range(db: Session, date_type: str, date_input: datetime, user_id: int):
    notification = []
    if date_type == 'Day':
        date_str = str(date_input.strftime("%Y%m%d"))
        notification = crud.get_notification_by_type(db, user_id, date_str, date_type)
    if date_type == 'Week':
        start_week, end_week = utils.get_day_of_week(date_input)

        date_str = str(start_week.strftime("%Y%m%d")) + "_" + str(end_week.strftime("%Y%m%d"))
        notification = crud.get_notification_by_type(db, user_id, date_str, date_type)
    if date_type == 'Month':
        start_month = date_input.replace(day=1)
        date_str = str(start_month.strftime("%Y%m"))
        notification = crud.get_notification_by_type(db, user_id, date_str, date_type)
    if date_type == 'Year':
        start_year = date(date_input.year, 1, 1)
        date_str = str(start_year.strftime("%Y"))
        notification = crud.get_notification_by_type(db, user_id, date_str, date_type)
    if date_type == 'Term':
        start_term, end_term = utils.get_day_of_term(date_input)
        date_str = str(start_term.strftime("%Y%m")) + "_" + str(end_term.strftime("%Y%m"))
        notification = crud.get_notification_by_type(db, user_id, date_str, date_type)

    return sorted(list(map(lambda db_notification: schemas.NotificationBase(content_id=db_notification.content_id,
                                                                            content_type=db_notification.content_type,
                                                                            pre_rank=db_notification.pre_rank,
                                                                            cur_rank=db_notification.cur_rank,
                                                                            create_date=db_notification.create_date,
                                                                            user_id=db_notification.user_id),
                           notification)), key=lambda notifications: notifications.create_date, reverse=True)


def get_notifications_by_user(db: Session, date_input: datetime, user_id: int):
    date_input = date_input.strftime("%Y-%m-%d")
    notifications = crud.get_notification_by_user(db, user_id, date_input)
    # db_notification.content_type
    return sorted(list(
        map(lambda db_notification: schemas.NotificationView(
            content='Daily ranking change' if db_notification.content_type == 'Day' else db_notification.content_type + 'ly ranking change',
            cur_rank=db_notification.cur_rank,
            pre_rank=db_notification.pre_rank,
            create_date=db_notification.create_date),
            notifications)), key=lambda notification: notification.create_date, reverse=True)
