from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db          
from app import models, schemas, auth    

router = APIRouter(prefix="/user", tags=["User - Xem Menu & Đặt món"])


@router.get("/foods", response_model=List[schemas.FoodResponse])
def get_menu(db: Session = Depends(get_db)):
    return db.query(models.Food).filter(models.Food.is_available == True).all()


@router.post("/order", response_model=schemas.BillResponse)
def place_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    
    db_bill = db.query(models.Bill).filter(
        models.Bill.table_number == order.table_number,
        models.Bill.is_paid == False
    ).first()

    if not db_bill:
        db_bill = models.Bill(table_number=order.table_number, user_id=current_user.id, total_price=0.0, is_paid=False)
        db.add(db_bill)
        db.commit()
        db.refresh(db_bill)

    for item in order.items:
        food = db.query(models.Food).filter(models.Food.id == item.food_id, models.Food.is_available == True).first()
        if not food:
            raise HTTPException(status_code=404, detail=f"Món ăn ID {item.food_id} không tồn tại hoặc đã hết!")

        db_detail = db.query(models.BillDetail).filter(
            models.BillDetail.bill_id == db_bill.id,
            models.BillDetail.food_id == food.id
        ).first()

        if db_detail:
            db_detail.quantity += item.quantity  
        else:
            new_detail = models.BillDetail(
                bill_id=db_bill.id,
                food_id=food.id,
                quantity=item.quantity,
                price_at_order=food.price  
            )
            db.add(new_detail)

    db.commit()

    all_details = db.query(models.BillDetail).filter(models.BillDetail.bill_id == db_bill.id).all()
    total = sum(d.quantity * d.price_at_order for d in all_details)
    
    db_bill.total_price = total
    db.commit()
    db.refresh(db_bill)

    response_details = []
    for d in all_details:
        food_info = db.query(models.Food).filter(models.Food.id == d.food_id).first()
        response_details.append({
            "food_id": d.food_id,
            "food_name": food_info.name if food_info else "Món đã bị xóa",
            "quantity": d.quantity,
            "price_at_order": d.price_at_order
        })

    return {
        "id": db_bill.id,
        "table_number": db_bill.table_number,
        "total_price": db_bill.total_price,
        "is_paid": db_bill.is_paid,
        "create_at": db_bill.create_at,
        "details": response_details
    }