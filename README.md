
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
