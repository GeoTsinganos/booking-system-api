from rest_framework import serializers
from django.db import IntegrityError, transaction
from .models import Service, Availability, Booking
from django.contrib.auth.models import User

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    date = serializers.DateField(read_only=True)
    start_time = serializers.TimeField(read_only=True)
    end_time = serializers.TimeField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "username",
            "status",
            "notes",
            "service",
            "availability",
            "date",
            "start_time",
            "end_time",
        ]
        read_only_fields = ["user", "status", "username"]

    def validate(self, data):
        availability = data.get("availability")
        service = data.get("service")

        if not availability:
            raise serializers.ValidationError({"availability": "This field is required."})

        # Ensure selected slot belongs to selected service
        if service and availability.service_id != service.id:
            raise serializers.ValidationError({"availability": "Selected slot does not belong to this service."})

        # Same availability cannot be double-booked (OneToOne safety)
        existing = getattr(availability, "booking", None)  # related_name="booking"
        if existing and existing.status in ["PENDING", "CONFIRMED"]:
            raise serializers.ValidationError("This time slot is already booked.")

        # GLOBAL rule: no overlapping bookings regardless of service/user
        qs = Booking.objects.filter(
            status__in=["PENDING", "CONFIRMED"],
            availability__date=availability.date,
        ).filter(
            availability__start_time__lt=availability.end_time,
            availability__end_time__gt=availability.start_time,
        )

        # If update, exclude itself
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError("This time is already booked.")

        return data
    
    def create(self, validated_data):
        availability = validated_data.get("availability")

        # Snapshot date/time ώστε να μη χάνονται όταν availability γίνει None στο cancel
        if availability:
            validated_data["date"] = availability.date
            validated_data["start_time"] = availability.start_time
            validated_data["end_time"] = availability.end_time

        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError("This time slot is already booked.")

   
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email"]

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
