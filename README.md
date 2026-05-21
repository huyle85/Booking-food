Booking Food API

Một ứng dụng Backend hoàn chỉnh cho hệ thống đặt món ăn (Booking Food) được xây dựng bằng **FastAPI**, **SQLAlchemy**, và **Pydantic**. Dự án hỗ trợ đầy đủ các tính năng từ xác thực người dùng, phân quyền cho đến quản lý hóa đơn.

Tính năng 
- Xác thực người dùng (Authentication): Sử dụng hệ thống mã hóa mật khẩu bảo mật cao kết hợp với **JWT (JSON Web Token)** để cấp Access Token.
- Phân quyền người dùng (Authorization): Quản lý quyền truy cập linh hoạt thông qua thuộc tính `role` (`user`, `admin`).
- Quản lý dữ liệu mạnh mẽ: Thiết lập mối quan hệ chặt chẽ giữa các bảng trong Database (ví dụ: Mối quan hệ tự động xóa dữ liệu rác `cascade="all, delete-orphan"` giữa Hóa đơn và Chi tiết hóa đơn).
- Kiểm thử trực quan:** Tích hợp sẵn Swagger UI để test API trực tiếp một cách dễ dàng.

---

📁 Cấu trúc thư mục dự án
```text
Booking-food/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # Điểm khởi chạy ứng dụng (FastAPI Instance)
│   ├── database.py      # Cấu hình kết nối Cơ sở dữ liệu (SQLAlchemy)
│   ├── models.py        # Định nghĩa các bảng Database (ORM Models)
│   ├── schemas.py       # Định nghĩa cấu trúc dữ liệu đầu vào/đầu ra (Pydantic Models)
│   └── auth.py          # Xử lý Logic xác thực, băm mật khẩu & giải mã JWT Token
│
├── routers/
│   ├── __init__.py
│   ├── admin.py         # Các API dành riêng cho quản trị viên
│   └── user.py          # Các API dành cho người dùng thông thường
│
├── docs.txt             # Tài liệu ghi chú dự án
└── README.md            # Hướng dẫn sử dụng dự án
