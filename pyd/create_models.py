from pydantic import BaseModel, Field
from datetime import datetime

class RestaurantCreate(BaseModel):
    name:str = Field(..., example="Ресторан")
    address:str = Field(..., example="Улица такая-то Дом №5")
    phone:str = Field(..., example="+79000000000")

    class Config:
        orm_mode = True

class TableCreate(BaseModel):
    number:str = Field(..., example="15")
    seats:int = Field(..., gt = 0, example=5)

    restaurant_id:int = Field(..., gt=0, example=1)

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username:str = Field(..., example="Petya")
    password:str = Field(..., example="a54da6d4acdhg")

    class Config:
        orm_mode = True

class BookingCreate(BaseModel):
    booking_time:datetime = Field(..., example="2024-05-28 18:00")
    duration:int = Field(..., gt=0, example=60)

    user_id:int = Field(..., gt=0, example=1)
    table_id:int = Field(..., gt=0, example=1)

    class Config:
        orm_mode = True