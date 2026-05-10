# Varoq — Minimalistic Book Tracker for Uzbekistan

> **varoq** (Uzbek for "page") — The dedicated mobile-first app for tracking physical books in Uzbekistan.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.15-REST?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ About

Varoq is a focused, solo-developed physical book tracker built specifically for Uzbekistan's reading culture. It lets users scan books via barcode (ISBN), track reading progress, write reviews, and see what their friends are reading — without the bloat of global platforms like Goodreads.

## 🚀 Features

- **Phone + OTP Auth** (Eskiz.uz ready)
- **Barcode / ISBN scanning** → instant book lookup
- **Personal Shelf** with status (Want to Read / Reading / Finished / etc.)
- **Page-by-page progress tracking**
- **Star ratings + reviews**
- **Friends Activity Feed** (social layer)
- **Community-driven Uzbek book database**
- **Clean REST API** with JWT authentication

## 🛠 Tech Stack

- **Backend**: Django 6.0 + Django REST Framework
- **Database**: PostgreSQL (ready for Docker)
- **Auth**: Phone OTP + JWT (SimpleJWT)
- **Models**: Fully normalized (Books, Authors, UserBooks, Reviews, FeedEvents, etc.)
- **Architecture**: Clean apps structure + signals for auto feed

## 📱 API Endpoints (Ready for Flutter)

| Method | Endpoint                        | Description                     |
|--------|----------------------------------|---------------------------------|
| POST   | `/api/accounts/auth/send_otp/`   | Send OTP to phone              |
| POST   | `/api/accounts/auth/verify_otp/` | Verify OTP + get JWT tokens    |
| GET    | `/api/shelf/`                    | My shelf                       |
| POST   | `/api/shelf/add-by-isbn/`        | **Scan book** → add to shelf   |
| PATCH  | `/api/shelf/{id}/update_progress/` | Update current page         |
| POST   | `/api/reviews/`                  | Write review                   |
| GET    | `/api/feed/`                     | Friends activity feed          |
| GET    | `/api/books/books/`              | Browse books                   |
