from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Booking, Notification
from .tasks import deliver_notification, _message_for


@receiver(post_save, sender=Booking)
def create_booking_confirmation(sender, instance, created, **kwargs):
    """Create the confirmation regardless of whether a booking came from Admin or the API."""
    if not created or not instance.guest.accepts_email or not instance.guest.email:
        return
    subject, body = _message_for(instance, Notification.Type.BOOKING_CONFIRMATION)
    Notification.objects.create(
        hotel=instance.hotel,
        guest=instance.guest,
        booking=instance,
        channel=Notification.Channel.EMAIL,
        notification_type=Notification.Type.BOOKING_CONFIRMATION,
        subject=subject,
        body=body,
    )


@receiver(post_save, sender=Notification)
def queue_new_notification(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: deliver_notification.delay(instance.id))
