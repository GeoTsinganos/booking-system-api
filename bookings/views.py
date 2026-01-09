# Create your views here.

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from .models import Service, Availability, Booking
from .serializers import (ServiceSerializer, AvailabilitySerializer, BookingSerializer)
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from datetime import datetime

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]


class AvailabilityViewSet(ModelViewSet):
    queryset = Availability.objects.filter(is_active=True)
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        
        return Booking.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()

        if booking.user != request.user:
            raise PermissionDenied("You cannot cancel this booking.")
        
        booking_datetime = timezone.make_aware(
            datetime.combine(booking.availability.date, booking.availability.start_time))

        if booking_datetime <= timezone.now():
            raise PermissionDenied("Past bookings cannot be cancelled.")
        
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)