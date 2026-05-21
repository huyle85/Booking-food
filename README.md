Booking Food API

A complete Backend application for a food ordering and booking system built with **FastAPI**, **SQLAlchemy**, and **Pydantic**. This project includes essential features ranging from user authentication and role-based access control to complex relational database management.

---

## Key Features

- **User Authentication:** Implements a highly secure password-hashing mechanism combined with **JWT (JSON Web Tokens)** for issuing temporary Access Tokens.
- **Role-Based Authorization:** Flexible access management utilizing a `role` field (`user`, `admin`) to restrict or grant permissions to specific API routes.
- **Robust Data Relationships:** Utilizes SQLAlchemy ORM to handle data integrity, featuring an automated cleanup mechanism (`cascade="all, delete-orphan"`) between the `Bill` and `BillDetail` tables to prevent orphaned data.
- **Interactive API Documentation:** Built-in integration with Swagger UI, allowing you to test out all the API endpoints directly from your browser.

---

## 📁 Project Directory Structure

```text
Booking-food/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # Application entry point (FastAPI instance)
│   ├── database.py      # Database connection and session configuration (SQLAlchemy)
│   ├── models.py        # Database ORM model definitions (Tables)
│   ├── schemas.py       # Pydantic models for data validation (Request/Response bodies)
│   └── auth.py          # Authentication logic, password hashing & JWT handling
│
├── routers/
│   ├── __init__.py
│   ├── admin.py         # API endpoints reserved for administrators
│   └── user.py          # API endpoints for regular customers
│
├── docs.txt             # Project documentation notes
└── README.md            # Setup and project guide
