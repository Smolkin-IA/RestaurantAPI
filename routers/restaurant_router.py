from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
import pyd
from auth import AuthHandler
from typing import List
import re

router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"],
)

auth_handler = AuthHandler()

@router.get('/', response_model = List[pyd.RestaurantBase])
async def get_restaurants(db:Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).all()
    return restaurants


@router.post('/', response_model = pyd.RestaurantBase)
async def create_restaurants(restaurant_input:pyd.RestaurantCreate, db:Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant_input.name).first()
    if restaurant:
        raise HTTPException(status_code=404, detail="Restaurant already exists")
    
    phone_pattern = re.compile(r'^((\+7|7|8)+([0-9]){10})$')
    if not phone_pattern.match(restaurant_input.phone):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    restaurant_db = models.Restaurant(
        name = restaurant_input.name,
        address = restaurant_input.address,
        phone = restaurant_input.phone
    )

    db.add(restaurant_db)
    db.commit()
    
    return restaurant_db


@router.put('/{restaurant_id}', response_model = pyd.RestaurantBase)
async def update_restaurants(restaurant_id:int, restaurant_input:pyd.RestaurantCreate, db:Session = Depends(get_db),
                             current_user:str = Depends(auth_handler.auth_wrapper)):
    restaurant_db = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant_db:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    name = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant_input.name).first()
    if name:
        raise HTTPException(status_code=404, detail="Restaurant already exists")
    
    restaurant_db.name = restaurant_input.name

    db.commit()

    return restaurant_db


@router.delete('/{restaurant_id}')
async def delete_restaurants(restaurant_id:int, db:Session = Depends(get_db),
                             current_user:str = Depends(auth_handler.auth_wrapper)):
    restaurant_db = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

    if not restaurant_db:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    db.delete(restaurant_db)
    db.commit()

    return {"message":"Restaurant deleted"}

