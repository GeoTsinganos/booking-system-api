# Booking System API

A RESTful Booking System backend built with Django REST Framework, featuring JWT authentication, role-based access control, and robust business rules such as availability management and prevention of double bookings.

This project was developed as a final assignment and simulates a real-world booking platform backend.

---

## 🚀 Features

- User registration & login using JWT authentication
- Role-based access control (authenticated users)
- Service management
- Availability time slots per service
- Booking creation linked to users, services, and availability
- Prevention of double booking (business rule enforced)
- View bookings per user (`/api/my-bookings/`)
- Booking cancellation with rules:
  - Only the booking owner can cancel
  - Past bookings cannot be cancelled
- Fully documented API with Swagger (OpenAPI)

---

## 🛠 Tech Stack

- Python 3
- Django
- Django REST Framework
- Simple JWT
- MySQL
- drf-yasg (Swagger documentation)

---

## 📂 Project Structure

booking_system/
├── bookings/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ └── urls.py
├── booking_system/
│ ├── settings.py
│ ├── urls.py
│ └── ...
└── manage.py

---

## 🔐 Authentication

Authentication is handled via JWT.

### Register

POST /api/auth/register/

### Login

POST /api/auth/login/

Use the returned **access token** as:
Authorization: Bearer <token>

---

## 📌 API Endpoints (Main)

### Services

GET /api/services/
POST /api/services/

### Availabilities

GET /api/availabilities/
POST /api/availabilities/

### Bookings

POST /api/bookings/
GET /api/bookings/
DELETE /api/bookings/{id}/

### My Bookings

GET /api/my-bookings/

---

## ❌ Business Rules

- A time slot cannot be booked more than once
- Users can only view their own bookings
- Users can only cancel their own bookings
- Past bookings cannot be cancelled

---

## 📄 API Documentation

Swagger UI is available at:

http://127.0.0.1:8000/swagger/

---

## ⚙️ Setup Instructions

1. Clone the repository
2. Create virtual environment
3. Install dependencies:

pip install -r requirements.txt

4. Configure MySQL database in `settings.py`
5. Run migrations:

python manage.py migrate

6. Run server:

python manage.py runserver

---

## 🎓 Author

Developed as part of a final project assignment to demonstrate backend development skills, REST API design, authentication, and business logic implementation.
