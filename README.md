# Booking System API

A RESTful Booking System backend built with **Django REST Framework**, featuring **JWT authentication**, **role-based access control**, and advanced business rules such as **dynamic availability generation**, **global conflict prevention**, and a complete **booking lifecycle**.

This project was developed as a final assignment and simulates a real-world booking platform backend with both **user** and **admin** capabilities.

---

## 🚀 Live Deployment (Railway)

- **API Base URL:** https://booking-system.up.railway.app
- **Swagger UI:** https://booking-system.up.railway.app/swagger/
- **Admin Panel:** https://booking-system.up.railway.app/admin/

The application is deployed on Railway and runs using Gunicorn with a production `start.sh` entrypoint.

---

## ✨ Features

### Authentication & Users
- User registration (username, email, first name, last name)
- JWT authentication (access & refresh tokens)
- Secure password handling
- Role-based permissions (User / Admin)

### Services & Availability
- Service management
- Dynamic generation of availability slots **on demand**
- Time slots generated per service and date (e.g. 09:00–17:00, 30-minute slots)
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
- Fully documented REST API using **Swagger (OpenAPI)**

---

## 🧰 Tech Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- MySQL
- drf-yasg (Swagger documentation)

---

## 📂 Project Structure

1.  [] booking_system/
2.  [] ├── bookings/
3.  [] │ ├── models.py
4.  [] │ ├── serializers.py
5.  [] │ ├── views.py
6.  [] │ ├── admin.py
7.  [] │ ├── apps.py
8.  [] │ └── urls.py
9.  [] ├── booking_system/
10. [] │ ├── settings.py
11. [] │ ├── urls.py
12. [] │ ├── asgi.py
13. [] │ └── wsgi.py
14. [] ├── fixtures/
15. [] │ └── seed.json
16. [] ├── Procfile
17. [] ├── start.sh
18. [] └── manage.py

---

## 🔐 Authentication

Authentication is handled via **JWT**.

### Register

`POST /api/auth/register/`

### Login

`POST /api/auth/login/`

Use the returned access token in requests:

Authorization: Bearer <access_token>

---

## 📌 Main API Endpoints

### Services

- `GET /api/services/`
- `POST /api/services/` (admin)

### Availability (generated dynamically)

- `GET /api/services/{id}/available-slots/?date=YYYY-MM-DD`

### Bookings

- `POST /api/bookings/`
- `GET /api/bookings/`
- `PATCH /api/bookings/{id}/cancel/`
- `POST /api/bookings/{id}/confirm/` (admin)

### My Bookings

- `GET /api/my-bookings/`

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

### Swagger UI is available at:

- **Production Swagger:** https://booking-system.up.railway.app/swagger/
- **Local Swagger:** http://127.0.0.1:8000/swagger/

---

## ⚙️ Setup Instructions (Local)

1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies:

`pip install -r requirements.txt`

4. Configure MySQL database in `settings.py` (MySQL or SQLite)
5. Run migrations:

`python manage.py migrate`

6. Create admin user:

`python manage.py createsuperuser`

7. Run server:

`python manage.py runserver`

---

## 🔐 Environment Variables (Production)

| Variable               | Description                   |
| ---------------------- | ----------------------------- |
| `DEBUG`                | `False`                       |
| `SECRET_KEY`           | Django secret key             |
| `DATABASE_URL`         | MySQL connection string       |
| `ALLOWED_HOSTS`        | booking-system.up.railway.app |
| `CORS_ALLOWED_ORIGINS` | Frontend domain(s)            |
| `CSRF_TRUSTED_ORIGINS` | Backend & frontend domains    |

### **Important** (Railway HTTPS proxy):

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

---

## 🌱 Seed Data (Fixtures)

### The project includes initial seed data:

`python manage.py loaddata fixtures/seed.json`

**On Windows, ensure fixtures are saved as UTF-8 without BOM.**

---

## 🛠️ Railway Notes
- The production app is started via start.sh
- Database seeding should be executed once on a fresh database
- After seeding, restore the normal start command

---

## 🎓 Author

Developed as part of a final project assignment to demonstrate:

- Backend architecture & API design
- Authentication & authorization
- Complex business logic enforcement
- Real-world booking system behavior
- production deployment
