from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    bills = relationship("Bill", back_populates="customer")

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    bill_details = relationship("BillDetail", back_populates="food")

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer, nullable=False, index=True)
    total_price = Column(Float, default=0.0)
    is_paid = Column(Boolean, default=False)
    create_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer = relationship("User", back_populates="bills")
    details = relationship("BillDetail", back_populates="bill", cascade="all, delete-orphan") #delete bill is not exist detail bill okkk

class BillDetail(Base):
    __tablename__ = "bill_details"
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price_at_order = Column(Float, nullable=False)
    bill = relationship("Bill", back_populates="details")
    food = relationship("Food", back_populates="bill_details")