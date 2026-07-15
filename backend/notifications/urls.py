from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, GuestViewSet, BookingViewSet, NotificationViewSet, NotificationTemplateViewSet
router = DefaultRouter()
router.register('hotels', HotelViewSet)
router.register('guests', GuestViewSet)
router.register('bookings', BookingViewSet)
router.register('notifications', NotificationViewSet)
router.register('templates', NotificationTemplateViewSet)
urlpatterns = router.urls
