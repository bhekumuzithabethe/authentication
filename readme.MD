# Django Auth System 🔐

A full-featured Django authentication system with secure email verification and password reset functionality. Built to offer a production-ready starting point for any web application requiring user registration and authentication.

## ✨ Features
## Features

- **User Signup with Email Verification:** New users must verify their email address before accessing protected features.
- **Login/Logout:** Secure authentication using Django’s built-in mechanisms.
- **Password Reset:** Users can request a password reset link sent to their verified email.
- **Customizable Email Templates:** Modify email subjects and content to match your branding.
- **Front-End Flexibility:** Integrates smoothly with both Django templates and front-end frameworks via API endpoints.



## 🛠️ Tech Stack

- Python 3.10+
- Django 4.x
- PostgreSQL (or SQLite for development)
- SMTP-compatible email backend (e.g. Gmail, SendGrid)
- Optional: Django Rest Framework, Celery, Redis

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/bhekumuzithabethe/authentication.git
cd authentication 
```

### 2. Create a virtual environment
### On windows

- On Linux and Mac
```python -m venv venv
    venv/bin/activate
```
- On Linux and Mac
```virtualenv venv venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Set Up Environment Variables
- Create a .env file and configure it like this:
```
SECRET_KEY=your_django_secret
DEBUG=True
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=noreply@example.com
```

### 5. Run migrations
```
python manage.py migrate
```

### 6. Start the Development Server
```
python manage.py runserver
```
