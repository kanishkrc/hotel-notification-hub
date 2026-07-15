from django.contrib import admin
from .models import Hotel, Guest, Booking, Notification, NotificationTemplate
admin.site.register([Hotel, Guest, Booking, Notification, NotificationTemplate])
