<div align="center">

# 🐾 PetCareHub

### One roof. Five roles. Every pet, taken care of.

*A full-stack Django platform where customers book vets, shop for pet supplies, and track deliveries — while vets, vendors, delivery agents, and admins each run their own side of the show.*

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-07405E?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Razorpay](https://img.shields.io/badge/Payments-Razorpay-0C2451)](https://razorpay.com/)
[![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)](LICENSE)
[![NOC Certified](https://img.shields.io/badge/Adoption%20Partner-NOC%20Certified-28a745)](#-a-real-world-partnership)

</div>

---

## 🐕 What is this, exactly?

Most college Django projects stop at one login and a CRUD table. PetCareHub doesn't.

It's built like a real pet-care marketplace would be — **five separate roles**, each with its own dashboard, its own permissions, and its own reason to log in:

| Role | What they're here for |
|---|---|
| 🧑 **Customer** | Shop for pet products, book a vet, track orders |
| 🩺 **Vet** | Manage a schedule, accept appointments, get verified |
| 🏪 **Vendor** | List products, manage stock, watch orders roll in |
| 🚴 **Delivery Boy** | Pick up the queue, mark deliveries done |
| 🛠️ **Admin** | See and control literally everything above |

Everything from OTP-based password resets to Razorpay checkout to area-wise vet search was built to *work*, not just demo well.

---

## 🏆 A Real-World Partnership

This isn't a fictional "adopt a pet" page for show. PetCareHub's adoption section is backed by an actual animal-welfare organization:

- 📜 A **No Objection Certificate** from **Adoption Home Ahmedabad**, authorizing PetCareHub to list their verified rescue animals.
- 🤝 A **Letter of Appreciation** recognizing the platform's contribution to responsible adoption.

Both documents are viewable right from the in-app **Adoption** page. Big thanks to **Naitik Bhatt** and the team at [@adoptionhome_ahmedabad](https://instagram.com/adoptionhome_ahmedabad) for trusting a student project with something real.

---

## ✨ Feature Tour

**For the Customer**
- Browse, search, cart, and wishlist pet products
- Book vet appointments filtered by area / pincode
- Checkout securely via **Razorpay**
- Full order + appointment history from their profile
- Forgot-password flow via emailed OTP (Gmail SMTP)

**For the Vet**
- Personal dashboard with a live schedule
- Accept, reject, or complete appointment requests
- Document upload for admin verification before going live

**For the Vendor**
- Own product catalog — add, edit, retire listings with images & categories
- Order visibility scoped to just their own products

**For the Delivery Boy**
- A clean queue of what needs delivering, and where
- One-tap status updates as orders move

**For the Admin**
- A single dashboard commanding all four other roles
- Approve or reject incoming Vet & Vendor sign-ups
- Full CRUD control over areas, categories, products, gallery, and feedback
- Every table in the system, exportable and searchable

---
[![View PDF](https://img.shields.io/badge/PDF-View_Full_Documentation-red?style=for-the-badge&logo=adobeacrobatreader)](./SCREEN_LAYOUTS.pdf)

---

## 🧰 Built With

| Layer | Technology |
|---|---|
| Backend | Django 5.2 (Python) |
| Database | SQLite (dev) |
| Frontend | HTML5, CSS3, Bootstrap, JavaScript, jQuery, Swiper.js |
| Auth | Custom role-based auth — hashed passwords + middleware route guards |
| Payments | Razorpay |
| Email | Django SMTP backend (Gmail) for OTP flows |
| Config | `python-dotenv` for environment-based secrets |

---

## 🏗️ How It's Organized

```
petcare/
├── petcare/         # Project settings, root URLs
├── test2/           # Admin panel app (dashboard, master tables)
├── client/          # Customer-facing app (shop, cart, appointments)
├── vet/             # Vet dashboard app
├── vendor/          # Vendor dashboard app
├── deliveryboy/     # Delivery agent app
├── media/           # User-uploaded files (product images, profile pics)
├── requirements.txt
└── manage.py
```

Each role lives as its own self-contained Django app — its own `*_urls.py`, `*_views.py`, templates, and static assets. Nothing bleeds into anything else.

---

## 🚀 Running It Locally

**Prerequisites:** Python 3.10+ and pip.

**1. Clone it**
```bash
git clone https://github.com/vraj537/petcare-hub.git
cd petcare-hub
```

**2. Spin up a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux
```

**3. Install the dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your environment file**
```bash
cp .env.example .env       # macOS/Linux
copy .env.example .env     # Windows
```
Open `.env` and fill in:
- `DJANGO_SECRET_KEY` — any random string
- `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` — a Gmail address + [App Password](https://myaccount.google.com/apppasswords), only needed if you want OTP emails to actually send

**5. Migrate the database**
```bash
python manage.py migrate
```

**6. Run it**
```bash
python manage.py runserver
```
Then open `http://127.0.0.1:8000/`

---

## 🔐 Security Notes

- Every secret (Django key, email credentials) loads from a local `.env` via `python-dotenv` — nothing hardcoded, nothing committed.
- Passwords are hashed with Django's built-in `make_password` / `check_password`.
- Each dashboard is fenced off by its own middleware guard (`client/middleware.py`, `test2/middleware.py`, and friends).

---

## 🗺️ Where This Could Go Next

- Swap SQLite for PostgreSQL in production
- Add automated tests with `pytest-django`
- Containerize with Docker for one-command setup
- Expose a REST API layer for a future mobile app

---

## 📄 License

**All Rights Reserved** — Copyright (c) 2026 PetCareHub. See [LICENSE](LICENSE) for the full text.

This project is **not** open-source. No permission is granted to copy, reproduce, redistribute, modify, or reuse this software, its source code, or any part of it — for personal, academic, or commercial purposes — without prior written permission from the copyright holder.

---

## 👥 Built By

**Vraj Rathod** — [@vraj537](https://github.com/vraj537)
**Ansh** — [@Anshu073](https://github.com/Anshu073)

A two-person final-year BCA capstone project, built from the ground up together. Open to a conversation about the architecture — feel free to reach out.
