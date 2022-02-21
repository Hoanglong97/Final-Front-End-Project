import calendar
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from controller import ranking as ranking_controller
from models import schemas
from models.dbconfig import get_db
from utils import utils
from .auth import get_user_info

router = APIRouter()


@router.post('/day', tags=["ranking"], response_model=schemas.RankingInfo)
async def ranking_day(input_date: str = Form(...),
                      current_user: schemas.User = Depends(get_user_info),
                      db: Session = Depends(get_db)):
    start_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    start_date_object = start_date.replace(hour=0).replace(minute=0).replace(microsecond=0)
    # Valid input sample: 2021-01-04 10:00:00
    end_date_object = start_date.replace(hour=23).replace(minute=0).replace(microsecond=0)
    if start_date_object > end_date_object:
        print("start_date is greater than end_date")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="start_date is greater than end_date")
    return ranking_controller.ranking(db=db, current_user=current_user, start_date=start_date_object,
                                      end_date=end_date_object)


@router.post('/week', tags=["ranking"], response_model=schemas.RankingInfo)
async def ranking_week(input_date: str = Form(...),
                       current_user: schemas.User = Depends(get_user_info),
                       db: Session = Depends(get_db)):
    input_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    start_date_object, end_date_object = utils.get_day_of_week(input_date)
    start_date_object = start_date_object.replace(hour=0).replace(minute=0).replace(microsecond=0)
    end_date_object = end_date_object.replace(hour=23).replace(minute=59).replace(microsecond=59)

    return ranking_controller.ranking(db=db, current_user=current_user,
                                      start_date=start_date_object, end_date=end_date_object)


@router.post('/period', tags=["ranking"], response_model=schemas.RankingInfo)
async def ranking_in_range(start_date: str = Form(...),
                           end_date: str = Form(...),
                           current_user: schemas.User = Depends(get_user_info),
                           db: Session = Depends(get_db)):
    # Validate input sample: 2021-01-01 10:00:00
    start_date_object = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    # Valid input sample: 2021-01-04 10:00:00
    end_date_object = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    if start_date_object > end_date_object:
        print("start_date is greater than end_date")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="start_date is greater than end_date")

    return ranking_controller.ranking(db=db, current_user=current_user,
                                      start_date=start_date_object, end_date=end_date_object)


@router.post('/month', tags=["ranking"], response_model=schemas.RankingInfo)
async def ranking_month(input_date: str = Form(...),
                        current_user: schemas.User = Depends(get_user_info),
                        db: Session = Depends(get_db)):
    # Validate input sample: 2021-01-01 10:00:00
    start_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    start_date_object = start_date.replace(day=1).replace(hour=0).replace(minute=0).replace(microsecond=0)
    # Valid input sample: 2021-01-04 10:00:00
    last_day_of_month = calendar.monthrange(start_date.year, start_date.month)[1]
    end_date_object = start_date.replace(day=last_day_of_month) \
        .replace(hour=0).replace(minute=0) \
        .replace(microsecond=0)

    if start_date_object > end_date_object:
        print("start_date is greater than end_date")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="start_date is greater than end_date")

    if start_date_object.month != end_date_object.month:
        print("month of start_date and end_date is different")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="month of start_date and end_date is different")
    return ranking_controller.ranking(db=db, current_user=current_user, start_date=start_date_object,
                                      end_date=end_date_object)


@router.post('/year', tags=["ranking"], response_model=schemas.RankingInfo)
async def ranking_year(input_date: str = Form(...),
                       current_user: schemas.User = Depends(get_user_info),
                       db: Session = Depends(get_db)):
    # Validate input sample: 2021-01-01 10:00:00
    start_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    start_date_object = datetime(start_date.year, 1, 1)
    # Valid input sample: 2021-01-04 10:00:00
    end_date_object = datetime(start_date.year, 12, 31)
    if start_date_object > end_date_object:
        print("start_date is greater than end_date")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="start_date is greater than end_date")
    return ranking_controller.ranking(db=db, current_user=current_user, start_date=start_date_object,
                                      end_date=end_date_object)


@router.post('/term', tags=["ranking"], response_model=schemas.RankingInfo)
async def ranking_term(input_date: str = Form(...),
                       current_user: schemas.User = Depends(get_user_info),
                       db: Session = Depends(get_db)):
    # There are two term :
    #                    First term start from 01/10 - next year 30/03
    #                    Second term start from 01/04 - 30/09
    input_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    start_date_object, end_date_object = utils.get_day_of_term(input_date)
    if start_date_object > end_date_object:
        print("start_date is greater than end_date")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="start_date is greater than end_date")
    return ranking_controller.ranking(db=db, current_user=current_user, start_date=start_date_object,
                                      end_date=end_date_object)


@router.post('/ranking_calculate', tags=["test"], response_model=schemas.Result)
async def ranking_calculate(db: Session = Depends(get_db)):
    # Validate input sample: 2021-01-01 10:00:00
    start_date_object = datetime.strptime("2021-01-01 10:00:00", "%Y-%m-%d %H:%M:%S")
    # Valid input sample: 2021-01-04 10:00:00
    end_date_object = datetime.strptime("2021-01-04 10:00:00", "%Y-%m-%d %H:%M:%S")
    print(ranking_controller.ranking_calculate(db, start_date_object, end_date_object))
    return schemas.Result(result='OK')
