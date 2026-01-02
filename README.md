# PetShopRoyal (Django E‑Commerce)

A Django-based e-commerce web app with product catalog, variants (size/color), cart & checkout, and basic content features (blog, contact, sitemap).

## Key Features
- Product catalog with categories, tags, rich descriptions (CKEditor), and image thumbnails
- Product variants (size/color) and discount pricing
- Cart operations (add/remove/update) and item count endpoint
- Checkout flow with delivery pricing by weight and coupon support
- User accounts + profile (address/phone) and favorites/compare
- Blog list/detail pages
- Sitemap generation for product pages

## Tech Stack
- Django (server-rendered templates)
- SQLite by default; optional Postgres via environment variables
- django-ckeditor, django-taggit, sorl-thumbnail, django-filter
- Jalali date support (django-jalali / jdatetime)

## Local Setup

### 1) Create a virtualenv + install deps
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment variables
Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

### 3) Run migrations + start the server
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Optional: Postgres
If `POSTGRES_DB` is set, the app will use Postgres. Otherwise it falls back to SQLite.
(You’ll need a running Postgres instance and the `psycopg2-binary` dependency, included in requirements.)

## Security Notes
- Do **not** commit secrets (SMTP passwords, Django secret key, etc.).
- This repo is configured to read secrets from environment variables.
