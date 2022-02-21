from datetime import datetime
from typing import List

from fastapi import APIRouter, Query, Form, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session

from controller import notification as notification_controller
from models import schemas
from models.dbconfig import get_db
from routes.auth import get_user_info

router = APIRouter()


@router.get("/", tags=["notification"], response_model=List[schemas.NotificationBase])
async def get_all_notification(user_id: int, db: Session = Depends(get_db)):
    return notification_controller.get_notifications(user_id, db)


@router.get("/type", tags=["notification"], response_model=List[schemas.NotificationBase])
async def get_all_notification_by_range(date_input: datetime,
                                        date_type=Query("Week", enum=["Day", "Week", "Month", "Year", "Term"]),
                                        current_user: schemas.User = Depends(get_user_info),
                                        db: Session = Depends(get_db)):
    return notification_controller.get_notifications_in_range(db, date_type, date_input, current_user.id)


@router.post("/user", tags=["notification"], response_model=List[schemas.NotificationView])
async def get_notification_by_user(date_input: str = Form(...),
                                   current_user: schemas.User = Depends(get_user_info),
                                   db: Session = Depends(get_db)):
    date_input = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
    return notification_controller.get_notifications_by_user(db, date_input, current_user.id)
