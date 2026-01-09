from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, AvailabilityViewSet, BookingViewSet, RegisterView, MyBookingsView
from django.urls import path


router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = router.urls + [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('my-bookings/', MyBookingsView.as_view()),
]
