from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base

class Restaurant(Base):
    __tablename__='restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)

class Table(Base):
    __tablename__ = 'tables'
    
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    number = Column(String(255), nullable=False)
    seats = Column(Integer, nullable=False)

    restaurant = relationship('Restaurant', backref='tables')

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)


class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    table_id = Column(Integer, ForeignKey('tables.id'), nullable=False)
    booking_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)

    user = relationship('User', backref='bookings')
    table = relationship('Table', backref='bookings')

