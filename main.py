from fastapi import FastAPI
from routers import booking_router, restaurant_router, table_router, user_router

app = FastAPI()

app.include_router(booking_router)
app.include_router(restaurant_router)
app.include_router(table_router)
app.include_router(user_router)