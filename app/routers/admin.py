from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["Admin - Quản lý món ăn"]
)

# 1. API: Thêm món ăn mới (Chỉ Admin mới có quyền)
@router.post("/foods", response_model=schemas.FoodResponse, status_code=status.HTTP_201_CREATED)
def create_food(
    food_in: schemas.FoodCreate,  # Nhận dữ liệu JSON từ Body gửi lên (KHÔNG dùng Depends ở đây)
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)  # Xác thực quyền Token Admin
):
    # Kiểm tra phân quyền: Phải là admin mới cho qua
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Bạn không có quyền thực hiện hành động này"
        )
        
    # Tạo đối tượng Food để lưu xuống database SQL Server
    new_food = models.Food(
        name=food_in.name,
        price=food_in.price,
        is_available=food_in.is_available
    )
    
    try:
        db.add(new_food)
        db.commit()
        db.refresh(new_food)
        return new_food
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lưu vào Database: {str(e)}"
        )


# 2. API: Xem danh sách tất cả món ăn (Dành cho Admin quản lý)
@router.get("/foods", response_model=list[schemas.FoodResponse])
def get_all_foods_admin(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền")
        
    foods = db.query(models.Food).all()
    return foods


# 3. API: Xóa món ăn theo ID
@router.delete("/foods/{food_id}")
def delete_food(
    food_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền")
        
    food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy món ăn để xóa")
        
    try:
        db.delete(food)
        db.commit()
        return {"message": f"Đã xóa món ăn có ID {food_id} thành công"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Không thể xóa món ăn do có ràng buộc dữ liệu: {str(e)}"
        )