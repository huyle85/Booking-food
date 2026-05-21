from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

class Token(BaseModel):
    access_token: str
    token_type: str

class FoodCreate(BaseModel):
    name: str
    price: float
    is_available: Optional[bool] = True

class FoodResponse(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool
    class Config:
        from_attributes = True

class OrderItem(BaseModel):
    food_id: int
    quantity: int

class OrderCreate(BaseModel):
    table_number: int
    items: List[OrderItem]

class BillDetailResponse(BaseModel):
    food_id: int
    food_name: str
    quantity: int
    price_at_order: float

    class Config:
        from_attributes = True

class BillResponse(BaseModel):
    id: int
    table_number: int
    total_price: float
    is_paid: bool
    create_at: datetime
    details: List[BillDetailResponse]

    class Config:
        from_attributes = True