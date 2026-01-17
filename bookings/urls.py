from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, AvailabilityViewSet, BookingViewSet, RegisterView, MyBookingsView, MeView
from django.urls import path


router = DefaultRouter()
router.register(r'services', ServiceViewSet,basename="service")
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = router.urls + [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('my-bookings/', MyBookingsView.as_view()),
    path("auth/me/", MeView.as_view(), name="me"),
]
