from rest_framework import serializers
from .models import Hotel, Guest, Booking, Notification, NotificationTemplate

class HotelSerializer(serializers.ModelSerializer):
    class Meta: model = Hotel; fields = '__all__'
class GuestSerializer(serializers.ModelSerializer):
    class Meta: model = Guest; fields = '__all__'
class BookingSerializer(serializers.ModelSerializer):
    class Meta: model = Booking; fields = '__all__'
class NotificationSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest.full_name', read_only=True)
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    class Meta: model = Notification; fields = '__all__'
class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta: model = NotificationTemplate; fields = '__all__'
