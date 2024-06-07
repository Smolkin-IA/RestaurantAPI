from pydantic import BaseModel, Field
from datetime import datetime

class RestaurantBase(BaseModel):
    id:int = Field(..., gt = 0, example = 1)
    name:str = Field(..., example="Ресторан")
    address:str = Field(..., example="Улица такая-то Дом №5")
    phone:str = Field(..., example="+79000000000")

    class Config:
        orm_mode = True

class TableBase(BaseModel):
    id:int = Field(..., gt = 0, example = 1)
    number:str = Field(..., example="")
    seats:int = Field(..., gt = 0, example=5)

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    id:int = Field(..., gt = 0, example = 1)
    username:str = Field(..., example="Petya")

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    id:int = Field(..., gt = 0, example = 1)
    booking_time:datetime = Field(..., example="2024-05-28 18:00")
    duration:int = Field(..., gt=0, example=60)

    class Config:
        orm_mode = True