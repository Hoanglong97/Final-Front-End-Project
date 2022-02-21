from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    # Phone number
    username: str
    # Customized nickname
    nick_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    create_at: Optional[datetime] = None
    avatar: Optional[str]

class Login(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    nick_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    avatar: Optional[str]
    password: Optional[str]


class User(UserBase):
    id: int


class UserInDB(User):
    hashed_password: str


class UserWithId(UserBase):
    id: int


class UserWithRank(UserBase):
    total_distance: float
    total_duration: float
    total_point: float


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class Result(BaseModel):
    result: str
    error: Optional[str] = None


class RecordBase(BaseModel):
    distance: float
    duration: float
    record_date: datetime
    image_path: Optional[str] = None
    point: float
    update_count: int


class RecordCreate(RecordBase):
    user_id: int


class Record(RecordBase):
    # id: Optional[int] = None
    id: int
    create_at: Optional[datetime] = None


class RankingInfo(BaseModel):
    my_rank: int
    list_user_with_rank: List[UserWithRank]


class Ranking_Day(BaseModel):
    day_id: str
    rank: int
    total_distance: float
    total_duration: float
    total_point: int
    user_id: int


class RankingDayUpdate(Ranking_Day):
    id: int


class Ranking_Week(BaseModel):
    week_id: str
    rank: int
    total_distance: float
    total_duration: float
    total_point: int
    user_id: int


class RankingWeekUpdate(Ranking_Week):
    id: int


class Ranking_Month(BaseModel):
    month_id: str
    rank: int
    total_distance: float
    total_duration: float
    total_point: int
    user_id: int


class RankingMonthUpdate(Ranking_Month):
    id: int


class Ranking_Term(BaseModel):
    term_id: str
    rank: int
    total_distance: float
    total_duration: float
    total_point: int
    user_id: int


class RankingTermUpdate(Ranking_Term):
    id: int


class Ranking_Year(BaseModel):
    year_id: str
    rank: int
    total_distance: float
    total_duration: float
    total_point: int
    user_id: int


class RankingYearUpdate(Ranking_Year):
    id: int


class NotificationBase(BaseModel):
    content_id: str
    content_type: str
    pre_rank: int
    cur_rank: int
    create_date: datetime
    user_id: int


class Notification(NotificationBase):
    id: int


class NotificationView(BaseModel):
    content: str
    cur_rank: int
    pre_rank: int
    create_date: datetime


class OverviewUser(BaseModel):
    nick_name: str
    distance: float
    duration: float
    month: float
    year: float


class Overview(BaseModel):
    distance: float
    dis_change: bool
    duration: float
    dur_change: bool
