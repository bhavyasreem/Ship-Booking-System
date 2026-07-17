# Nautica Ship Booking System

A premium, full-stack **Ship Booking System** designed with a modern glassmorphism aesthetic. It allows passengers to search voyages, select cabins, book tickets, make secure payments, and check history, while providing administrators with a complete fleet, schedule, passenger, booking, and transaction CRUD control panel.

---

## 🚀 Technology Stack

- **Frontend**: HTML5, CSS3 (Vanilla design, custom vars, responsive layouts), JavaScript (ES6), Fetch API
- **Backend**: Django REST Framework, Function-Based Views (FBV)
- **Database**: MongoDB Atlas (connected via `pymongo`)

---

## 📂 Project Folder Structure

```text
ShipBookingSystem/
│
├── Backend/
│   ├── settings.py      # Django configuration (CORS, REST Framework)
│   ├── urls.py          # API route maps for the 20 CRUD endpoints
│   ├── db.py            # MongoDB Atlas connection & ID counters helper
│   ├── views.py         # DRF function-based CRUD views
│   └── wsgi.py / asgi.py
│
├── Frontend/
│   ├── index.html       # Hero, Dynamic Search & Voucher offers
│   ├── login.html       # Secure sign-in with admin override checks
│   ├── register.html    # Profile registration
│   ├── ships.html       # Fleets/voyages search and listings
│   ├── ship_details.html# Interactive galleries & live cabin selection
│   ├── booking.html     # Pre-filled ticket reservation
│   ├── payment.html     # UPI & Card simulated transaction gateway
│   ├── booking_history.html# Trip filters (Upcoming vs Past) & cancellations
│   ├── passenger_dashboard.html# Passenger statistics, profile edits modal
│   ├── admin_dashboard.html# Administrator CRUD control tabs
│   ├── style.css        # Responsive dark-theme nautical stylesheet
│   └── script.js        # Global header/nav, authentication & fetch wrapper
│
├── manage.py            # Django administration utility
└── README.md
```

---
<img width="1911" height="988" alt="Screenshot 2026-07-17 151745" src="https://github.com/user-attachments/assets/303092bb-4332-4202-b46e-ee22ce72f7b3" />
<img width="1917" height="1005" alt="Screenshot 2026-07-17 151800" src="https://github.com/user-attachments/assets/93071de2-a486-4cf0-9dfb-b2395dd60bb6" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/d2bd9a4b-d669-4b8c-89aa-220cc17e676c" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/28b8d172-9cfc-4392-8488-f76de5a6c31e" />
<img width="1912" height="883" alt="image" src="https://github.com/user-attachments/assets/3f0368c2-ffdb-4d43-8725-11ba88e047ff" />




## 🔌 API Documentation (20 CRUD Endpoints)

| Module | Method | Endpoint | Description |
| :--- | :---: | :--- | :--- |
| **Passenger Management** | `POST` | `/passengers/add/` | Register new passenger profile |
| | `GET` | `/passengers/` | Fetch all registered passenger records |
| | `PUT` | `/passengers/update/<id>/` | Update details of a passenger |
| | `DELETE`| `/passengers/delete/<id>/`| Remove a passenger from the database |
| **Ship Management** | `POST` | `/ships/add/` | Add a new ship (fleet) |
| | `GET` | `/ships/` | Fetch all ship fleet records |
| | `PUT` | `/ships/update/<id>/` | Modify ship parameters (capacity, status) |
| | `DELETE`| `/ships/delete/<id>/` | Remove a ship from the fleet |
| **Route & Schedule** | `POST` | `/schedules/add/` | Create a new voyage schedule route |
| | `GET` | `/schedules/` | List all upcoming voyages |
| | `PUT` | `/schedules/update/<id>/` | Modify dates, times, or fares for a route |
| | `DELETE`| `/schedules/delete/<id>/` | Remove a schedule route |
| **Cabin/Ticket Booking**| `POST` | `/bookings/add/` | Create a booking reservation (Waiting) |
| | `GET` | `/bookings/` | Fetch all ticket bookings |
| | `PUT` | `/bookings/update/<id>/` | Modify booking status (Confirmed, Cancelled) |
| | `DELETE`| `/bookings/delete/<id>/` | Delete a booking record |
| **Payment Management** | `POST` | `/payments/add/` | Record transaction details |
| | `GET` | `/payments/` | Fetch list of all receipts |
| | `PUT` | `/payments/update/<id>/` | Update transaction state (Success, Failed) |
| | `DELETE`| `/payments/delete/<id>/` | Delete a payment transaction record |

---

## 🔑 Test Credentials

For testing and verification, the database is preloaded with the following logins:

### 👤 Passenger Profile
- **Email**: `rahul@gmail.com`
- **Password**: `....`
- **Actions**: Search journeys, select cabins, proceed to checkout, make payment, check upcoming trips, update password/profile.

### 🛡️ Administrator Panel
- **Email**: `admin@shipbooking.com`
- **Password**: `admin123`
- **Actions**: Perform CRUD modifications on Passengers, Ships, Routes, Bookings, and Payments with tabular views.

---

## ⚓ Pre-loaded Voyage Fleet & Routes

The system starts preloaded with **6 ships** and **10 Indian maritime voyages**:

1. **Ocean Paradise** (Cruise): Chennai Port ➔ Port Blair (INR 8,500)
2. **Sea Breeze Ferry** (Ferry): Gateway of India ➔ Elephanta Caves (INR 250)
3. **Ganges Queen** (River Cruise): Varanasi Port ➔ Patna Port (INR 4,500)
4. **Royal Vista** (Cruise): Mumbai Port ➔ Goa Port (INR 6,200)
5. **Adonia Yacht** (Yacht): Cochin Port ➔ Lakshadweep Port (INR 15,000)
6. **Ocean Paradise** (Cruise): Port Blair ➔ Chennai Port (INR 8,000)
7. **Royal Vista** (Cruise): Goa Port ➔ Mumbai Port (INR 6,000)
8. **Sindhudurg Express** (Ferry): Mumbai Port ➔ Diu Port (INR 1,200)
9. **Adonia Yacht** (Yacht): Lakshadweep Port ➔ Cochin Port (INR 14,000)
10. **Sea Breeze Ferry** (Ferry): Elephanta Caves ➔ Gateway of India (INR 250)

---

## 🛠️ Installation & Setup Instructions

### 1. Pre-requisites
Make sure you have Python 3.7+ installed.

### 2. Start the Backend API Server
Navigate to the root project directory and start the Django server:
```bash
python manage.py runserver
```
The backend server will run on `http://127.0.0.1:8000/`.

### 3. Start the Frontend Server
Serve the frontend using Python's static HTTP server (to bypass security policies on local files):
```bash
python -m http.server 8080 --directory Frontend
```
Open your browser and visit: `http://localhost:8080/index.html`.
