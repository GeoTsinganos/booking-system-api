# Booking System API

Ένα RESTful backend σύστημα κρατήσεων, υλοποιημένο με Django REST Framework, το οποίο υποστηρίζει JWT authentication, έλεγχο πρόσβασης χρηστών και επιχειρησιακούς κανόνες όπως διαχείριση διαθεσιμότητας και αποτροπή διπλών κρατήσεων.

Το project αναπτύχθηκε ως τελική εργασία και προσομοιώνει ένα πραγματικό σύστημα κρατήσεων.

---

## 🚀 Λειτουργίες

- Εγγραφή και σύνδεση χρηστών με JWT authentication
- Έλεγχος πρόσβασης (μόνο authenticated χρήστες)
- Διαχείριση υπηρεσιών (services)
- Διαχείριση διαθέσιμων χρονικών slots (availability) ανά υπηρεσία
- Δημιουργία κρατήσεων συνδεδεμένων με χρήστη, υπηρεσία και διαθεσιμότητα
- Αποτροπή διπλής κράτησης (business rule)
- Προβολή κρατήσεων ανά χρήστη (`/api/my-bookings/`)
- Ακύρωση κράτησης με κανόνες:
  - Μόνο ο ιδιοκτήτης της κράτησης μπορεί να την ακυρώσει
  - Δεν επιτρέπεται ακύρωση παρελθοντικών κρατήσεων
- Πλήρης τεκμηρίωση API με Swagger (OpenAPI)

---

## 🛠 Τεχνολογίες

- Python 3
- Django
- Django REST Framework
- Simple JWT
- MySQL
- drf-yasg (Swagger documentation)

---

## 📂 Δομή Project

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

Η αυθεντικοποίηση γίνεται με JWT tokens.

### Εγγραφή

POST /api/auth/register/

### Σύνδεση

POST /api/auth/login/

Χρήση token σε κάθε request:
Authorization: Bearer <token>

---

## 📌 Βασικά API Endpoints

### Υπηρεσίες

GET /api/services/
POST /api/services/

### Διαθεσιμότητα

GET /api/availabilities/
POST /api/availabilities/

### Κρατήσεις

POST /api/bookings/
GET /api/bookings/
DELETE /api/bookings/{id}/

### Οι κρατήσεις μου

GET /api/my-bookings/

---

## ❌ Επιχειρησιακοί Κανόνες

- Ένα χρονικό slot δεν μπορεί να κρατηθεί περισσότερες από μία φορές
- Οι χρήστες βλέπουν μόνο τις δικές τους κρατήσεις
- Η ακύρωση κράτησης επιτρέπεται μόνο από τον ιδιοκτήτη
- Δεν επιτρέπεται ακύρωση παρελθοντικών κρατήσεων

---

## 📄 Τεκμηρίωση API

Το Swagger UI είναι διαθέσιμο στη διεύθυνση:

http://127.0.0.1:8000/swagger/

---

## ⚙️ Οδηγίες Εγκατάστασης

1. Κλωνοποιήστε το repository
2. Δημιουργήστε virtual environment
3. Εγκαταστήστε τα dependencies:

pip install -r requirements.txt

4. Ρυθμίστε τη βάση δεδομένων MySQL στο `settings.py`
5. Εκτελέστε migrations:

python manage.py migrate

6. Εκκινήστε τον server:

python manage.py runserver

---

## 🎓 Δημιουργός

Το project αναπτύχθηκε ως τελική εργασία με στόχο την επίδειξη δεξιοτήτων backend ανάπτυξης, σχεδίασης REST APIs, authentication και υλοποίησης επιχειρησιακής λογικής.
