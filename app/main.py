from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import models, schemas, auth
from app.routers import admin, user 


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hệ thống Backend Đặt món Nhà hàng - FastAPI & SQL Server",
    description="Hệ thống hỗ trợ Admin quản lý menu, thanh toán hóa đơn và User đặt món cộng dồn theo bàn.",
    version="1.0.0"
)


app.include_router(admin.router)
app.include_router(user.router)


@app.post("/register")
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user_in.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username đã tồn tại")

    hashed_pwd = auth.hash_password(user_in.password) 
    new_user = models.User(
        username=user_in.username, 
        hash_password=hashed_pwd,  #
        role=user_in.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = auth.create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=schemas.Token, tags=["Xác thực hệ thống"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác!"
        )
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

