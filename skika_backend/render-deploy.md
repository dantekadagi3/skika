# Render Deployment Configuration
# This file contains deployment instructions for Render.com

## Build Command:
# pip install -r requirements-prod.txt

## Start Command:
# python manage.py migrate && python manage.py collectstatic --noinput && gunicorn skika_backend.wsgi:application

## Environment Variables (Set in Render Dashboard):
# SECRET_KEY=your-secret-key-here
# DEBUG=False
# ALLOWED_HOSTS=your-app-name.onrender.com
# DB_NAME=your-postgres-db-name
# DB_USER=your-postgres-username  
# DB_PASSWORD=your-postgres-password
# DB_HOST=your-postgres-host
# DB_PORT=5432
# AFRICASTALKING_USERNAME=your-username
# AFRICASTALKING_API_KEY=your-api-key
# AFRICASTALKING_SANDBOX=False

## Notes:
# 1. Use requirements-prod.txt for deployment (more stable dependencies)
# 2. Ensure PostgreSQL database is created and accessible
# 3. Set DEBUG=False for production
# 4. Add your Render app URL to ALLOWED_HOSTS
# 5. Configure Africa's Talking API credentials for SMS/USSD