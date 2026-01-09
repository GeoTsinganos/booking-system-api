from django.contrib import admin
from .models import Service, Availability, Booking

# Register your models here.

admin.site.register(Service)
admin.site.register(Availability)
admin.site.register(Booking)