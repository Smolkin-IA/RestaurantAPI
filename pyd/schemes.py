from .base_models import *

class TableScheme(TableBase):
    restaurant: RestaurantBase

class BookingScheme(BookingBase):
    user: UserBase
    table: TableBase
