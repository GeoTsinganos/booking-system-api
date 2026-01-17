# Booking System API

A RESTful Booking System backend built with **Django REST Framework**, featuring **JWT authentication**, **role-based access control**, and advanced business rules such as **dynamic availability generation**, **global conflict prevention**, and a complete **booking lifecycle**.

This project was developed as a final assignment and simulates a real-world booking platform backend with both **user** and **admin** capabilities.

---

## 🚀 Features

### Authentication & Users
- User registration with username, email, first name & last name
- JWT-based login (access & refresh tokens)
- Secure password handling
- Role-based permissions (User / Admin)

### Services & Availability
- Service management
- Dynamic generation of availability slots **on demand**
- Time slot generation per service/day (e.g. 09:00–17:00, 30-minute slots)
- Automatic reuse of slots after cancellation

### Bookings
- Booking creation linked to:
  - User
  - Service
  - Availability slot
- **Global conflict prevention**
  - No overlapping bookings across services
- **No double booking**
  - Enforced at serializer + database level

### Booking Lifecycle
- `PENDING` → `CONFIRMED` (admin action)
- `CANCELLED` → availability slot becomes reusable
- Past bookings cannot be cancelled

### Admin Capabilities
- View **all bookings**
- Confirm or cancel bookings
- Filter bookings by:
  - Service
  - Date
  - Status
  - Username

### Documentation
- Fully documented API using **Swagger (OpenAPI)**

---

## 🛠 Tech Stack

- Python 3
- Django
- Django REST Framework
- Simple JWT
- MySQL (production-ready)
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

Authentication is handled via **JWT**.

### Register

POST /api/auth/register/

### Login

POST /api/auth/login/

Use the returned access token in requests:
Authorization: Bearer <token>

---

## 📌 Main API Endpoints

### Services

GET /api/services/
POST /api/services/ (admin)

### Availability (generated dynamically)

GET /api/services/{id}/available-slots/?date=YYYY-MM-DD

### Bookings

POST /api/bookings/
GET /api/bookings/
PATCH /api/bookings/{id}/cancel/
POST /api/bookings/{id}/confirm/ (admin)

### My Bookings

GET /api/my-bookings/

---

## ❌ Business Rules

- A time slot cannot be booked more than once
- No overlapping bookings (global rule)
- Users can only view their own bookings
- Users can only cancel their own future bookings
- Past bookings cannot be cancelled
- Cancelled bookings free up availability automatically

---

## 📄 API Documentation

Swagger UI is available at:

http://127.0.0.1:8000/swagger/

---

## ⚙️ Setup Instructions (Local)

1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies:

pip install -r requirements.txt

4. Configure MySQL database in `settings.py` (MySQL or SQLite)
5. Run migrations:

python manage.py migrate

6. Create admin user:

python manage.py createsuperuser

7. Run server:

python manage.py runserver

---

## 🎓 Author

Developed as part of a final project assignment to demonstrate:

- Backend architecture & API design
- Authentication & authorization
- Complex business logic enforcement
- Real-world booking system behavior