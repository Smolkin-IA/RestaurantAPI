from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
import pyd
from auth import AuthHandler
from typing import List


router = APIRouter(
    prefix="/booking",
    tags=["Booking"],
)

auth_handler = AuthHandler()

@router.get('/', response_model = List[pyd.BookingBase])
async def get_bookings(db:Session = Depends(get_db)):
    bookings = db.query(models.Booking).all()
    return bookings

@router.post('/', response_model = pyd.BookingBase)
async def create_bookings(booking_input:pyd.BookingCreate, db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == booking_input.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    table = db.query(models.Table).filter(models.Table.id == booking_input.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    booking_db = models.Booking(
        user_id = booking_input.user_id,
        table_id = booking_input.table_id,
        booking_time = booking_input.booking_time,
        duration = booking_input.duration
    )

    db.add(booking_db)
    db.commit()
    
    return booking_db

@router.put('/{booking_id}', response_model = pyd.BookingBase)
async def update_bookings(booking_id:int, booking_input:pyd.BookingCreate, db:Session = Depends(get_db),
                             current_user:str = Depends(auth_handler.auth_wrapper)):
    booking_db = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    user = db.query(models.User).filter(models.User.id == booking_input.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    table = db.query(models.Table).filter(models.Table.id == booking_input.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    booking_db.user_id = booking_input.user_id
    booking_db.table_id = booking_input.table_id
    booking_db.booking_time = booking_input.booking_time
    booking_db.duration = booking_input.duration

    db.commit()

    return booking_db

@router.delete('/{booking_id}')
async def delete_bookings(booking_id:int, db:Session = Depends(get_db),
                             current_user:str = Depends(auth_handler.auth_wrapper)):
    booking_db = db.query(models.Booking).filter(models.Booking.id == booking_id).first()

    if not booking_db:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db.delete(booking_db)
    db.commit()

    return {"message":"Booking deleted"}