import calendar
import os
from datetime import datetime, timedelta


def file_base_name(file_name):
    if '.' in file_name:
        separator_index = file_name.index('.')
        base_name = file_name[:separator_index]
        return base_name
    else:
        return file_name


def path_base_name(path):
    file_name = os.path.basename(path)
    return file_base_name(file_name)


def get_index_by_condition(list_elements, condition):
    index_pos_list = []
    for i in range(len(list_elements)):
        if condition(list_elements[i]):
            index_pos_list.append(i)
    return index_pos_list


def get_day_of_week(date_object):
    start_of_week = date_object - timedelta(days=date_object.weekday())
    return start_of_week, start_of_week + timedelta(days=6)


def get_day_of_term(date_object):
    if 4 <= date_object.month <= 9:
        start_date_object = datetime(date_object.year, 4, 1)
        last_day_of_month = calendar.monthrange(date_object.year, 9)[1]
        end_date_object = datetime(date_object.year, 9, last_day_of_month)
    elif 10 <= date_object.month <= 12:
        start_date_object = datetime(date_object.year, 10, 1)
        last_day_of_month = calendar.monthrange(date_object.year + 1, 3)[1]
        end_date_object = datetime(date_object.year + 1, 3, last_day_of_month)
    else:
        start_date_object = datetime(date_object.year - 1, 10, 1)
        last_day_of_month = calendar.monthrange(date_object.year, 3)[1]
        end_date_object = datetime(date_object.year, 3, last_day_of_month)
    return start_date_object,end_date_object
