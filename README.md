# Hotel Notification Hub

An MVP notification management system for a multi-property luxury hotel group.

## What it does

- Keeps hotels, guests, bookings, templates, and notification delivery records in one place.
- Creates automated booking confirmation, pre-arrival, and post-stay notifications.
- Supports per-property templates, email/SMS/push consent preferences, delivery attempts, and retries.
- Sends work to Celery in the background; the MVP simulates delivery and records the result.
- Provides a React dashboard to see hotels and recent notifications.

## Run it

1. Install Docker Desktop and start it.
2. From this folder run `docker compose up --build`.
3. Open `http://localhost:5173` for the dashboard and `http://localhost:8000/api/` for the API.
4. Create an admin user: `docker compose exec backend python manage.py createsuperuser`, then visit `http://localhost:8000/admin/`.

## Testing

Run `docker compose exec backend coverage run manage.py test` followed by `docker compose exec backend coverage report`.

## Important next steps before production

Connect an approved email/SMS vendor, secure secrets in environment variables, add login/role permissions, and integrate the hotel PMS/booking system. Do not send promotional messages without recorded guest consent.
