from django.contrib import admin

# Register your models here.
from .models import Farm, SensorReading

admin.site.register(Farm)
admin.site.register(SensorReading)
