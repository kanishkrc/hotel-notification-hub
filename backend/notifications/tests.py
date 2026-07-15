from datetime import date, timedelta
from django.test import TestCase
from .models import Booking, Guest, Hotel, Notification
from .tasks import deliver_notification, schedule_stay_messages


class NotificationWorkflowTests(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(name='Aurum Palace', city='Jaipur', email_from='hello@aurum.test')
        self.guest = Guest.objects.create(full_name='Test Guest', email='guest@example.test')

    def test_booking_creates_confirmation(self):
        booking = Booking.objects.create(hotel=self.hotel, guest=self.guest, confirmation_code='TEST-100', check_in=date.today() + timedelta(days=1), check_out=date.today() + timedelta(days=2))
        notification = Notification.objects.get(booking=booking, notification_type=Notification.Type.BOOKING_CONFIRMATION)
        deliver_notification(notification.id)
        notification.refresh_from_db()
        self.assertEqual(notification.status, Notification.Status.SENT)
        self.assertEqual(notification.attempt_count, 1)

    def test_pre_arrival_campaign_creates_notification(self):
        booking = Booking.objects.create(hotel=self.hotel, guest=self.guest, confirmation_code='TEST-101', check_in=date.today() + timedelta(days=1), check_out=date.today() + timedelta(days=2))
        schedule_stay_messages()
        self.assertTrue(Notification.objects.filter(booking=booking, notification_type=Notification.Type.PRE_ARRIVAL).exists())
