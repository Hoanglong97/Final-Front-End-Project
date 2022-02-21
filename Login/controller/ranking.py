from datetime import datetime

from sqlalchemy.orm import Session

from controller import records as record_controller, users as user_controller
from models import schemas
from utils import utils


# Calculate user ranking when new record is added.
def ranking_calculate(db: Session, start_date: datetime, end_date: datetime):
    # Return ranking in week
    # Get list user from user_controller
    all_users = user_controller.get_all_users(db)
    for tmp_user in all_users:
        list_records = record_controller.get_all_records_in_range(db, tmp_user, start_date, end_date)
        tmp_total_distance = 0
        for tmp_record in list_records:
            tmp_total_distance += tmp_record.distance

    # Get list records of each user from database from start_date to end_date
    # Calculate total distance with total time of each user
    return schemas.Result(result='OK')


# Return list user with sorted ranking by total distance
def ranking_in_range(db: Session, start_date: datetime, end_date: datetime):
    # Return ranking in week
    tmp_ranking = []
    # Get list user from user_controller
    all_users = user_controller.get_all_users(db)
    for tmp_user in all_users:
        # Get list records of each user from database from start_date to end_date
        list_records = record_controller.get_all_records_in_range(db, tmp_user, start_date, end_date)
        if list_records:
            tmp_total_distance = 0
            tmp_total_duration = 0
            tmp_total_point = 0
            # Calculate total distance with total time of each user
            for tmp_record in list_records:
                tmp_total_distance += tmp_record.distance
                tmp_total_duration += tmp_record.duration
                tmp_total_point += tmp_record.point
            tmp_user_with_rank = schemas.UserWithRank(username=tmp_user.username,
                                                      nick_name=tmp_user.nick_name,
                                                      date_of_birth=tmp_user.date_of_birth,
                                                      create_at=tmp_user.create_at,
                                                      avatar=tmp_user.avatar,
                                                      total_point=tmp_total_point,
                                                      total_distance=tmp_total_distance,
                                                      total_duration=tmp_total_duration)
            tmp_ranking.append(tmp_user_with_rank)
    # Return list users with sorted position by duration
    return sorted(tmp_ranking, key=lambda user: user.total_distance, reverse=True)


def ranking_in_range_by_point(db: Session, start_date: datetime, end_date: datetime):
    # Return ranking in week
    tmp_ranking = []
    # Get list user from user_controller
    all_users = user_controller.get_all_users(db)
    for tmp_user in all_users:
        # Get list records of each user from database from start_date to end_date
        list_records = record_controller.get_all_records_in_range(db, tmp_user, start_date, end_date)
        if list_records:
            tmp_total_distance = 0
            tmp_total_duration = 0
            tmp_total_point = 0
            # Calculate total distance with total time of each user
            for tmp_record in list_records:
                tmp_total_distance += tmp_record.distance
                tmp_total_duration += tmp_record.duration
                tmp_total_point += tmp_record.point
            tmp_user_with_rank = schemas.UserWithRank(username=tmp_user.username,
                                                      nick_name=tmp_user.nick_name,
                                                      date_of_birth=tmp_user.date_of_birth,
                                                      create_at=tmp_user.create_at,
                                                      avatar=tmp_user.avatar,
                                                      total_point=tmp_total_point,
                                                      total_distance=tmp_total_distance,
                                                      total_duration=tmp_total_duration)
            tmp_ranking.append(tmp_user_with_rank)
    # Return list users with sorted position by duration
    return sorted(tmp_ranking, key=lambda user: user.total_point, reverse=True)


def my_rank(list_users: [schemas.UserWithRank], current_user: schemas.User):
    list_position_index = utils.get_index_by_condition(list_users,
                                                       lambda user: user.username == current_user.username)
    current_user_position = -1
    if len(list_position_index) > 0:
        current_user_position = list_position_index[0] + 1
    return current_user_position


def total_score(list_users: [schemas.UserWithRank], current_user: schemas.User):
    total_dis = total_dur = total_point = 0
    for i in range(len(list_users)):
        if list_users[i].username == current_user.username:
            total_dis = list_users[i].total_distance
            total_dur = list_users[i].total_duration
            total_point = list_users[i].total_point
    return total_dis, total_dur, total_point


# Return user ranking in a day
def ranking(db: Session, current_user: schemas.User, start_date: datetime, end_date: datetime):
    # Return ranking in day
    list_user_by_point_sorted = ranking_in_range_by_point(db, start_date, end_date)
    current_user_position = my_rank(list_user_by_point_sorted, current_user)
    return schemas.RankingInfo(my_rank=current_user_position,
                               list_user_with_rank=ranking_in_range_by_point(db, start_date, end_date))
