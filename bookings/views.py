# Create your views here.
from django.db.models import Q
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from .models import Service, Availability, Booking
from .serializers import ServiceSerializer, AvailabilitySerializer, BookingSerializer
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from datetime import datetime, time, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import RegisterSerializer
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "available_slots"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            name="date",
            in_=openapi.IN_QUERY,
            description="Date (YYYY-MM-DD)",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ]
)
    @action(detail=True, methods=["get"], url_path="available-slots")
    def available_slots(self, request, pk=None):
        """
        GET /api/services/{id}/available-slots/?date=YYYY-MM-DD
        Generates slots on demand (09:00–17:00 every 30') and returns only available ones.
        """
        service = self.get_object()
        date_str = request.query_params.get("date")

        if not date_str:
            return Response(
                {"detail": "date query param is required (YYYY-MM-DD)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"detail": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        SLOT_MINUTES = 30
        WORK_START = time(9, 0)
        WORK_END = time(17, 0)

        start_dt = datetime.combine(target_date, WORK_START)
        end_dt = datetime.combine(target_date, WORK_END)

        cur = start_dt
        to_create = []

        while cur + timedelta(minutes=SLOT_MINUTES) <= end_dt:
            s = cur.time()
            e = (cur + timedelta(minutes=SLOT_MINUTES)).time()

            exists = Availability.objects.filter(
                service=service,
                date=target_date,
                start_time=s,
                end_time=e,
            ).exists()

            if not exists:
                to_create.append(
                    Availability(
                        service=service,
                        date=target_date,
                        start_time=s,
                        end_time=e,
                        is_active=True,
                    )
                )

            cur += timedelta(minutes=SLOT_MINUTES)

        if to_create:
            Availability.objects.bulk_create(to_create)

        active_ranges = list(
            Booking.objects.filter(
                status__in=["PENDING", "CONFIRMED"],
                availability__date=target_date,
                availability__isnull=False,
            )
            .select_related("availability")
            .values_list("availability__start_time", "availability__end_time")
        )

        def overlaps(start_a, end_a, start_b, end_b):
            return start_a < end_b and end_a > start_b

        available_slots = []
        for slot in Availability.objects.filter(
            service=service,
            date=target_date,
            is_active=True,
        ).order_by("start_time"):
            conflict = any(
                overlaps(slot.start_time, slot.end_time, b_start, b_end)
                for (b_start, b_end) in active_ranges
            )
            if not conflict:
                available_slots.append(slot)

        return Response(
            AvailabilitySerializer(available_slots, many=True).data,
            status=status.HTTP_200_OK,
        )

class AvailabilityViewSet(ModelViewSet):
    queryset = Availability.objects.filter(is_active=True)
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Booking.objects.none()

        qs = Booking.objects.all()

        # Admin sees all
        if self.request.user.is_staff or self.request.user.is_superuser:
            # optional filters
            date_str = self.request.query_params.get("date")
            service_id = self.request.query_params.get("service")
            status_val = self.request.query_params.get("status")
            username = self.request.query_params.get("username")

            if status_val:
                qs = qs.filter(status=status_val)

            if service_id:
                qs = qs.filter(service_id=service_id)

            if date_str:
                qs = qs.filter(date=date_str)

            if username:
                qs = qs.filter(user__username__icontains=username)

            return qs.order_by("-id")

        # User sees his own
        return qs.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("Bookings cannot be deleted. Use cancel instead.")

    @action(detail=True, methods=["post"], url_path="cancel", permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if not request.user.is_staff and booking.user_id != request.user.id:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        if booking.status == "CANCELLED":
            return Response({"detail": "Already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        if booking.availability_id is not None:
            naive_dt = datetime.combine(booking.availability.date, booking.availability.start_time)
            booking_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())

            if booking_dt <= timezone.now():
                return Response(
                    {"detail": "You cannot cancel a past booking."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        booking.status = "CANCELLED"
        booking.availability = None  # frees slot (OneToOne)
        booking.save(update_fields=["status", "availability"])

        return Response(self.get_serializer(booking).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="confirm", permission_classes=[IsAdminUser])
    def confirm(self, request, pk=None):
        booking = self.get_object()

        if booking.status == "CANCELLED":
            return Response(
                {"detail": "Cannot confirm a cancelled booking."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = "CONFIRMED"
        booking.save(update_fields=["status"])
        return Response(self.get_serializer(booking).data, status=status.HTTP_200_OK)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )

class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            "id": u.id,
            "username": u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
            "is_staff": u.is_staff,
            "is_superuser": u.is_superuser,
        })