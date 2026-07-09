# Easy Learn Academy — Training Management Portal

A full-featured Django web application for managing college technical training programs, trainer sessions, invoices, and expenses.

## 🌐 Live Preview
> Run locally at: **http://127.0.0.1:8001/**

---

## 🔑 Login Credentials

### Admin (Stephen Jebadurai)
| Field | Value |
|-------|-------|
| URL | `/login/` |
| Username | `admin` |
| Password | `adminpassword123` |

### Trainer Account
| Field | Value |
|-------|-------|
| URL | `/login/` |
| Username | `stephenjebadurai` |
| Password | `trainerpassword123` |

---

## 🚀 Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Stephen-jd/Easy-Learn-_-Website.git
cd Easy-Learn-_-Website
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django pillow xhtml2pdf openpyxl
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Seed Demo Data
```bash
python manage.py seed_data
```

### 6. Run Server
```bash
python manage.py runserver 8001
```

Open → **http://127.0.0.1:8001/**

---

## 📁 Project Structure

```
Easy Learn/
├── core/                    # Main Django app
│   ├── templates/core/      # HTML templates
│   │   ├── landing_gate.html    ← Public marketing website
│   │   ├── landing.html         ← Admin operations dashboard
│   │   ├── trainer_dashboard.html
│   │   ├── admin_dashboard.html
│   │   └── login.html
│   ├── static/core/images/  # Logo & slideshow images
│   ├── models.py            # Project, Trainer, Workload, Invoice, Expense
│   ├── views.py             # All views with role-based access
│   └── urls.py
├── easy_learn/              # Django project config
├── manage.py
└── README.md
```

---

## 🎯 Key Features

### Public Website
- Full marketing landing page (Hero, Programs, Partner Colleges, Testimonials)
- 100% Online training programs
- Login button in navbar corner (single entry for admin + trainer)

### Admin Features
- Operations dashboard with live stats
- Approve / reject trainer sign-ups
- View all trainer profiles, Aadhaar docs, bank details
- Manage projects (RYMEC, SMVITM, BLDEA, ASBLDEA)
- Track & categorize all training expenses
- Download Excel expense reports

### Trainer Features
- Log daily session workloads (up to 3 sessions/day)
- Upload class notes (PDF)
- Auto-generate monthly invoices (daily or monthly rate)
- Download invoice PDFs
- Manage bank details & UPI

---

## 🏫 Partner Colleges

| College | Location | Status |
|---------|----------|--------|
| RYMEC | Bellary, Karnataka | Active |
| SMVITM | Udupi, Karnataka | Active |
| BLDEA | Vijayapur, Karnataka | Active |
| ASBLDEA | Bijapur, Karnataka | Active |

---

## 🛠 Tech Stack

- **Backend**: Django 6.0, Python 3.x
- **Database**: SQLite (development)
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **PDF**: xhtml2pdf
- **Excel**: openpyxl

---

*Built by Stephen Jebadurai — Easy Learn Academy © 2026*
