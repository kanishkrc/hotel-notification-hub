from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from .models import Booking, Notification, NotificationTemplate

@shared_task
def deliver_notification(notification_id):
    notification = Notification.objects.get(id=notification_id)
    try:
        # Replace this simulated delivery with a provider integration (SES / SMS / push).
        notification.status = Notification.Status.SENT
        notification.sent_at = timezone.now()
        notification.attempt_count += 1
        notification.failure_reason = ''
        notification.save(update_fields=['status', 'sent_at', 'attempt_count', 'failure_reason'])
        return notification.id
    except Exception as exc:
        notification.status = Notification.Status.FAILED
        notification.attempt_count += 1
        notification.failure_reason = str(exc)
        notification.save(update_fields=['status', 'attempt_count', 'failure_reason'])
        raise


def _message_for(booking, notification_type):
    template = NotificationTemplate.objects.filter(
        hotel=booking.hotel, notification_type=notification_type,
        channel=Notification.Channel.EMAIL, is_active=True,
    ).first()
    context = {'guest_name': booking.guest.full_name, 'hotel_name': booking.hotel.name,
               'confirmation_code': booking.confirmation_code, 'check_in': booking.check_in,
               'check_out': booking.check_out}
    if template:
        return template.subject.format(**context), template.body.format(**context)
    defaults = {
        Notification.Type.BOOKING_CONFIRMATION: ('Your stay is confirmed', 'Dear {guest_name}, your booking {confirmation_code} at {hotel_name} is confirmed.'),
        Notification.Type.PRE_ARRIVAL: ('Your stay begins tomorrow', 'Dear {guest_name}, we look forward to welcoming you to {hotel_name} tomorrow.'),
        Notification.Type.POST_STAY: ('Thank you for staying with us', 'Dear {guest_name}, thank you for choosing {hotel_name}. We hope to welcome you again soon.'),
    }
    subject, body = defaults[notification_type]
    return subject.format(**context), body.format(**context)


@shared_task
def schedule_stay_messages():
    """Hourly check for pre-arrival (one day before) and post-stay messages."""
    today = timezone.localdate()
    created_count = 0
    campaigns = [(today + timedelta(days=1), Notification.Type.PRE_ARRIVAL, 'check_in'),
                 (today, Notification.Type.POST_STAY, 'check_out')]
    for target_date, notification_type, date_field in campaigns:
        for booking in Booking.objects.select_related('hotel', 'guest').filter(**{date_field: target_date}):
            if not booking.guest.accepts_email or not booking.guest.email:
                continue
            subject, body = _message_for(booking, notification_type)
            _, created = Notification.objects.get_or_create(
                booking=booking, notification_type=notification_type, channel=Notification.Channel.EMAIL,
                defaults={'hotel': booking.hotel, 'guest': booking.guest, 'subject': subject, 'body': body},
            )
            created_count += int(created)
    return created_count
