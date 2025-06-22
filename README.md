# DMS

A Django and Dash project providing an interactive data management interface.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Start the development server:
   ```bash
   python manage.py runserver
   ```
   
Before running any Django commands, set a secret key in the environment:
```bash
export DJANGO_SECRET_KEY='your-strong-secret-key'
```
