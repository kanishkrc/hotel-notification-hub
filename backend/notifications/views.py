from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Hotel, Guest, Booking, Notification, NotificationTemplate
from .serializers import HotelSerializer, GuestSerializer, BookingSerializer, NotificationSerializer, NotificationTemplateSerializer
from .tasks import deliver_notification, schedule_stay_messages

class HotelViewSet(viewsets.ModelViewSet): queryset = Hotel.objects.all().order_by('name'); serializer_class = HotelSerializer
class GuestViewSet(viewsets.ModelViewSet): queryset = Guest.objects.all().order_by('full_name'); serializer_class = GuestSerializer
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('hotel', 'guest').all().order_by('-created_at'); serializer_class = BookingSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related('hotel', 'guest').all().order_by('-created_at'); serializer_class = NotificationSerializer
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        deliver_notification.delay(pk)
        return Response({'detail': 'Notification queued for delivery.'}, status=202)
    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        notification = self.get_object()
        notification.status = Notification.Status.QUEUED
        notification.save(update_fields=['status'])
        deliver_notification.delay(notification.id)
        return Response({'detail': 'Notification retry queued.'}, status=202)
    @action(detail=False, methods=['post'], url_path='run-stay-campaigns')
    def run_stay_campaigns(self, request):
        schedule_stay_messages.delay()
        return Response({'detail': 'Pre-arrival and post-stay campaigns queued.'}, status=202)

class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.select_related('hotel').all().order_by('hotel__name', 'notification_type')
    serializer_class = NotificationTemplateSerializer
