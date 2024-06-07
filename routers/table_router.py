from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
import pyd
from auth import AuthHandler
from typing import List

router = APIRouter(
    prefix="/table",
    tags=["Table"],
)

auth_handler = AuthHandler()

@router.get('/', response_model = List[pyd.TableBase])
async def get_tables(db:Session = Depends(get_db)):
    tables = db.query(models.Table).all()
    return tables

@router.post('/', response_model = pyd.TableBase)
async def create_tables(table_input:pyd.TableCreate, db:Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.number == table_input.number).first()
    if table:
        raise HTTPException(status_code=404, detail="Table already exists")
    
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == table_input.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    table_db = models.Table(
        number = table_input.number,
        restaurant_id = table_input.restaurant_id,
        seats = table_input.seats
    )

    db.add(table_db)
    db.commit()
    
    return table_db

@router.put('/{table_id}', response_model = pyd.TableBase)
async def update_tables(table_id:int, table_input:pyd.TableCreate, db:Session = Depends(get_db),
                        current_user:str = Depends(auth_handler.auth_wrapper)):
    table_db = db.query(models.Table).filter(models.Table.id == table_id).first()
    if not table_db:
        raise HTTPException(status_code=404, detail="Table not found")
    
    number = db.query(models.Table).filter(models.Table.number == table_input.number).first()
    if number:
        raise HTTPException(status_code=404, detail="Table already exists")
    
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == table_input.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    table_db.number = table_input.number
    table_db.restaurant_id = table_input.restaurant_id
    table_db.seats = table_input.seats

    db.commit()

    return table_db

@router.delete('/{table_id}')
async def delete_tables(table_id:int, db:Session = Depends(get_db),
                        current_user:str = Depends(auth_handler.auth_wrapper)):
    
    table_db = db.query(models.Table).filter(models.Table.id == table_id).first()
    if not table_db:
        raise HTTPException(status_code=404, detail="Table not found")
    
    db.delete(table_db)
    db.commit()

    return {"message":"Table deleted"}