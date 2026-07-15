from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=80)
    email_from = models.EmailField()
    is_active = models.BooleanField(default=True)
    def __str__(self): return f'{self.name} — {self.city}'

class Guest(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    accepts_email = models.BooleanField(default=True)
    accepts_sms = models.BooleanField(default=False)
    accepts_push = models.BooleanField(default=False)
    def __str__(self): return self.full_name

class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, related_name='bookings')
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name='bookings')
    confirmation_code = models.CharField(max_length=32, unique=True)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    class Channel(models.TextChoices): EMAIL = 'email', 'Email'; SMS = 'sms', 'SMS'; PUSH = 'push', 'Push'
    class Status(models.TextChoices): QUEUED = 'queued', 'Queued'; SENT = 'sent', 'Sent'; FAILED = 'failed', 'Failed'
    class Type(models.TextChoices):
        BOOKING_CONFIRMATION = 'booking_confirmation', 'Booking confirmation'
        PRE_ARRIVAL = 'pre_arrival', 'Pre-arrival'
        POST_STAY = 'post_stay', 'Post-stay'
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, related_name='notifications')
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name='notifications')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.CharField(max_length=10, choices=Channel.choices)
    notification_type = models.CharField(max_length=30, choices=Type.choices, default=Type.BOOKING_CONFIRMATION)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.QUEUED)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    attempt_count = models.PositiveIntegerField(default=0)
    failure_reason = models.TextField(blank=True)


class NotificationTemplate(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='templates')
    notification_type = models.CharField(max_length=30, choices=Notification.Type.choices)
    channel = models.CharField(max_length=10, choices=Notification.Channel.choices, default=Notification.Channel.EMAIL)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField(help_text='Use {guest_name}, {hotel_name}, {confirmation_code}, {check_in}, or {check_out}.')
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['hotel', 'notification_type', 'channel'], name='unique_hotel_template')]

    def __str__(self): return f'{self.hotel.name}: {self.get_notification_type_display()}'
