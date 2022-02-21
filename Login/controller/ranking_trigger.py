from calendar import monthrange
from datetime import datetime, date

from sqlalchemy.orm import Session

from controller import ranking as ranking_controller
from controller import users as user_controller
from models import crud, schemas
from utils import utils


def ranking_day(db: Session, datetime_object: datetime):
    day_id = datetime_object.strftime("%Y%m%d")
    list_day = crud.get_ranking_day(db, day_id)
    sorted_users = ranking_controller.ranking_in_range_by_point(db, datetime_object, datetime_object)
    all_users = user_controller.get_all_users(db)

    for tmp_user in all_users:
        tmp_rank = ranking_controller.my_rank(sorted_users, tmp_user)
        if tmp_rank >= 0:
            exist = 0
            if list_day:
                for tmp_day in list_day:
                    if tmp_user.id == tmp_day.user_id:
                        exist += 1
                        if tmp_day.rank != tmp_rank:
                            notification = schemas.NotificationBase(
                                content_id=day_id,
                                content_type="Day",
                                pre_rank=tmp_day.rank,
                                cur_rank=tmp_rank,
                                create_date=datetime.utcnow(),
                                user_id=tmp_user.id
                            )
                            crud.create_notification(db, notification, tmp_user.id)
                            total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                               tmp_user)
                            crud.update_ranking_day(db, tmp_day, tmp_rank, total_dis, total_dur, total_point)
                if exist == 0:
                    notification = schemas.NotificationBase(
                        content_id=day_id,
                        content_type="Day",
                        pre_rank=0,
                        cur_rank=tmp_rank,
                        create_date=datetime.utcnow(),
                        user_id=tmp_user.id
                    )
                    crud.create_notification(db, notification, tmp_user.id)
                    total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                       tmp_user)
                    crud.create_ranking_day(db, day_id, tmp_user.id, tmp_rank, total_dis, total_dur, total_point)
            else:
                notification = schemas.NotificationBase(
                    content_id=day_id,
                    content_type="Day",
                    pre_rank=0,
                    cur_rank=tmp_rank,
                    create_date=datetime.utcnow(),
                    user_id=tmp_user.id
                )
                crud.create_notification(db, notification, tmp_user.id)
                total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                   tmp_user)
                crud.create_ranking_day(db, day_id, tmp_user.id, tmp_rank, total_dis, total_dur, total_point)


def ranking_week(db: Session, datetime_object: datetime):
    start_week, end_week = utils.get_day_of_week(datetime_object)
    week_id = start_week.strftime("%Y%m%d") + "_" + end_week.strftime("%Y%m%d")
    list_week = crud.get_ranking_week(db, week_id)
    sorted_users = ranking_controller.ranking_in_range(db, start_week, end_week)
    all_users = user_controller.get_all_users(db)

    for tmp_user in all_users:
        tmp_rank = ranking_controller.my_rank(sorted_users, tmp_user)
        if tmp_rank >= 0:
            exist = 0
            if list_week:
                for tmp_week in list_week:
                    if tmp_user.id == tmp_week.user_id:
                        exist += 1
                        if tmp_week.rank != tmp_rank:
                            notification = schemas.NotificationBase(
                                content_id=week_id,
                                content_type="Week",
                                pre_rank=tmp_week.rank,
                                cur_rank=tmp_rank,
                                create_date=datetime.utcnow(),
                                user_id=tmp_user.id
                            )
                            crud.create_notification(db, notification, tmp_user.id)
                            total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                               tmp_user)
                            crud.update_ranking_week(db, tmp_week, tmp_rank, total_dis, total_dur, total_point)
                if exist == 0:
                    notification = schemas.NotificationBase(
                        content_id=week_id,
                        content_type="Week",
                        pre_rank=0,
                        cur_rank=tmp_rank,
                        create_date=datetime.utcnow(),
                        user_id=tmp_user.id
                    )
                    crud.create_notification(db, notification, tmp_user.id)
                    total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                       tmp_user)
                    crud.create_ranking_week(db, week_id, tmp_user.id, tmp_rank, total_dis, total_dur, total_point)
            else:
                notification = schemas.NotificationBase(
                    content_id=week_id,
                    content_type="Week",
                    pre_rank=0,
                    cur_rank=tmp_rank,
                    create_date=datetime.utcnow(),
                    user_id=tmp_user.id
                )
                crud.create_notification(db, notification, tmp_user.id)
                total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                   tmp_user)
                crud.create_ranking_week(db, week_id, tmp_user.id, tmp_rank, total_dis, total_dur, total_point)


def ranking_month(db: Session, datetime_object: datetime):
    start_month = datetime_object.replace(day=1)
    end_month = datetime_object.replace(day=monthrange(datetime_object.year, datetime_object.month)[1])
    month_id = start_month.strftime("%Y%m")
    list_month = crud.get_ranking_month(db, month_id)
    sorted_users = ranking_controller.ranking_in_range(db, start_month, end_month)
    all_users = user_controller.get_all_users(db)

    for tmp_user in all_users:
        tmp_rank = ranking_controller.my_rank(sorted_users, tmp_user)
        if tmp_rank >= 0:
            exist = 0
            if list_month:
                for tmp_month in list_month:
                    if tmp_user.id == tmp_month.user_id:
                        exist += 1
                        if tmp_month.rank != tmp_rank:
                            notification = schemas.NotificationBase(
                                content_id=month_id,
                                content_type="Month",
                                pre_rank=tmp_month.rank,
                                cur_rank=tmp_rank,
                                create_date=datetime.utcnow(),
                                user_id=tmp_user.id
                            )
                            crud.create_notification(db, notification, tmp_user.id)
                            total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                               tmp_user)
                            crud.update_ranking_month(db, tmp_month, tmp_rank, total_dis, total_dur, total_point)
                if exist == 0:
                    notification = schemas.NotificationBase(
                        content_id=month_id,
                        content_type="Month",
                        pre_rank=0,
                        cur_rank=tmp_rank,
                        create_date=datetime.utcnow(),
                        user_id=tmp_user.id
                    )
                    crud.create_notification(db, notification, tmp_user.id)
                    total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                       tmp_user)
                    crud.create_ranking_month(db, month_id, tmp_user.id, tmp_rank, total_dis, total_dur, total_point)
            else:
                notification = schemas.NotificationBase(
                    content_id=month_id,
                    content_type="Month",
                    pre_rank=0,
                    cur_rank=tmp_rank,
                    create_date=datetime.utcnow(),
                    user_id=tmp_user.id
                )
                crud.create_notification(db, notification, tmp_user.id)
                total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                   tmp_user)
                crud.create_ranking_month(db, month_id, tmp_user.id, tmp_rank, total_dis, total_dur, total_point)


def ranking_term(db: Session, datetime_object: datetime):
    start_term, end_term = utils.get_day_of_term(datetime_object)
    term_id = start_term.strftime("%Y%m") + "_" + end_term.strftime("%Y%m")
    list_term = crud.get_ranking_term(db, term_id)
    sorted_users = ranking_controller.ranking_in_range(db, start_term, end_term)
    all_users = user_controller.get_all_users(db)

    for tmp_user in all_users:
        tmp_rank = ranking_controller.my_rank(sorted_users, tmp_user)
        if tmp_rank >= 0:
            exist = 0
            if list_term:
                for tmp_term in list_term:
                    if tmp_user.id == tmp_term.user_id:
                        exist += 1
                        if tmp_term.rank != tmp_rank:
                            notification = schemas.NotificationBase(
                                content_id=term_id,
                                content_type="Term",
                                pre_rank=tmp_term.rank,
                                cur_rank=tmp_rank,
                                create_date=datetime.utcnow(),
                                user_id=tmp_user.id
                            )
                            crud.create_notification(db, notification, tmp_user.id)
                            total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                               tmp_user)
                            crud.update_ranking_term(db, tmp_term, tmp_rank, total_dis, total_dur, total_point)
                if exist == 0:
                    notification = schemas.NotificationBase(
                        content_id=term_id,
                        content_type="Term",
                        pre_rank=0,
                        cur_rank=tmp_rank,
                        create_date=datetime.utcnow(),
                        user_id=tmp_user.id
                    )
                    crud.create_notification(db, notification, tmp_user.id)
                    total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                       tmp_user)
                    crud.create_ranking_term(db, term_id, tmp_user.id, tmp_rank, total_dis, total_dur, total_point)
            else:
                notification = schemas.NotificationBase(
                    content_id=term_id,
                    content_type="Term",
                    pre_rank=0,
                    cur_rank=tmp_rank,
                    create_date=datetime.utcnow(),
                    user_id=tmp_user.id
                )
                crud.create_notification(db, notification, tmp_user.id)
                total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                   tmp_user)
                crud.create_ranking_term(db, term_id, tmp_user.id, tmp_rank, total_dis, total_dur, total_point)


def ranking_year(db: Session, datetime_object: datetime):
    start_year = date(datetime_object.year, 1, 1)
    end_year = date(datetime_object.year, 12, 31)
    year_id = start_year.strftime("%Y")
    list_year = crud.get_ranking_year(db, year_id)
    sorted_users = ranking_controller.ranking_in_range(db, start_year, end_year)
    all_users = user_controller.get_all_users(db)

    for tmp_user in all_users:
        tmp_rank = ranking_controller.my_rank(sorted_users, tmp_user)
        if tmp_rank >= 0:
            exist = 0
            if list_year:
                for tmp_year in list_year:
                    if tmp_user.id == tmp_year.user_id:
                        exist += 1
                        if tmp_year.rank != tmp_rank:
                            notification = schemas.NotificationBase(
                                content_id=year_id,
                                content_type="Year",
                                pre_rank=tmp_year.rank,
                                cur_rank=tmp_rank,
                                create_date=datetime.utcnow(),
                                user_id=tmp_user.id
                            )
                            crud.create_notification(db, notification, tmp_user.id)
                            total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                               tmp_user)
                            crud.update_ranking_year(db, tmp_year, tmp_rank, total_dis, total_dur, total_point)
                if exist == 0:
                    notification = schemas.NotificationBase(
                        content_id=year_id,
                        content_type="Year",
                        pre_rank=0,
                        cur_rank=tmp_rank,
                        create_date=datetime.utcnow(),
                        user_id=tmp_user.id
                    )
                    crud.create_notification(db, notification, tmp_user.id)
                    total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                       tmp_user)
                    crud.create_ranking_year(db, year_id, tmp_user.id, tmp_rank, total_dis, total_dur, total_point)
            else:
                notification = schemas.NotificationBase(
                    content_id=year_id,
                    content_type="Year",
                    pre_rank=0,
                    cur_rank=tmp_rank,
                    create_date=datetime.utcnow(),
                    user_id=tmp_user.id
                )
                crud.create_notification(db, notification, tmp_user.id)
                total_dis, total_dur, total_point = ranking_controller.total_score(sorted_users,
                                                                                   tmp_user)
                crud.create_ranking_year(db, year_id, tmp_user.id, tmp_rank, total_dis, total_dur, total_point)
