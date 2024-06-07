from sqlalchemy.orm import Session
from database import engine
import models
from datetime import datetime

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

with Session(bind = engine) as session:
    r1 = models.Restaurant(name="Ресторан 1",address="Улица 1, дом №12",phone="+7-922-222-22-22")
    r2 = models.Restaurant(name="Ресторан 2",address="Улица 2, дом №21",phone="+7-933-333-33-33")
    t1 = models.Table(restaurant=r1, number="123", seats=5)
    t2 = models.Table(restaurant=r2, number="321", seats=6)
    u1 = models.User(username="user1", password="qwerty")
    u2 = models.User(username="user2", password="123456")
    b1 = models.Booking(user=u1, table=t1, booking_time=datetime(2024,6,1,11,00), duration="60")
    b2 = models.Booking(user=u2, table=t2, booking_time=datetime(2024,6,3,15,30), duration="120")

    session.add_all([r1,r2,t1,t2,u1,u2,b1,b2])
    session.commit()
