from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from .dbconfig import Base


class User(Base):
    __tablename__ = 'users'
    # User id: Database auto increment
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    nick_name = Column(String, unique=True, index=True)
    date_of_birth = Column(String)
    avatar = Column(String)
    create_date = Column(DateTime, default=datetime.utcnow())
    record_list = relationship('Record', back_populates='user')
    notification_list = relationship('Notification', back_populates='user')
    day_ranking = relationship('Ranking_Day', back_populates='user')
    week_ranking = relationship('Ranking_Week', back_populates='user')
    month_ranking = relationship('Ranking_Month', back_populates='user')
    term_ranking = relationship('Ranking_Term', back_populates='user')
    year_ranking = relationship('Ranking_Year', back_populates='user')


class Record(Base):
    __tablename__ = 'records'
    # Id of record
    id = Column(Integer, primary_key=True, index=True)
    # Running distance
    distance = Column(Float)
    # Running duration
    duration = Column(Float)
    # Record date
    record_date = Column(DateTime)
    # Path to evidence image
    image = Column(String)
    point = Column(Float)
    update_count = Column(Integer)
    create_date = Column(DateTime, default=datetime.utcnow())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='record_list')


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(String)
    content_type = Column(String)
    pre_rank = Column(Integer)
    cur_rank = Column(Integer)
    create_date = Column(DateTime, default=datetime.utcnow())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='notification_list')


class Ranking_Day(Base):
    __tablename__ = 'ranking_day'
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(String)
    rank = Column(Integer)
    total_distance = Column(Float)
    total_duration = Column(Float)
    total_point = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='day_ranking')


class Ranking_Week(Base):
    __tablename__ = 'ranking_week'
    id = Column(Integer, primary_key=True, index=True)
    week_id = Column(String)
    rank = Column(Integer)
    total_distance = Column(Float)
    total_duration = Column(Float)
    total_point = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='week_ranking')


class Ranking_Month(Base):
    __tablename__ = 'ranking_month'
    id = Column(Integer, primary_key=True, index=True)
    month_id = Column(String)
    rank = Column(Integer)
    total_distance = Column(Float)
    total_duration = Column(Float)
    total_point = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='month_ranking')


class Ranking_Term(Base):
    __tablename__ = 'ranking_term'
    id = Column(Integer, primary_key=True, index=True)
    term_id = Column(String)
    rank = Column(Integer)
    total_distance = Column(Float)
    total_duration = Column(Float)
    total_point = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='term_ranking')


class Ranking_Year(Base):
    __tablename__ = 'ranking_year'
    id = Column(Integer, primary_key=True, index=True)
    year_id = Column(String)
    rank = Column(Integer)
    total_distance = Column(Float)
    total_duration = Column(Float)
    total_point = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='year_ranking')
