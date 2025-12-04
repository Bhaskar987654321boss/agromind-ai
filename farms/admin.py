from django.contrib import admin
from .models import Field, SensorLog

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'area_hectares', 'soil_type', 'created_at')
    search_fields = ('name', 'owner__username', 'soil_type')

@admin.register(SensorLog)
class SensorLogAdmin(admin.ModelAdmin):
    list_display = ('field', 'timestamp', 'temperature', 'humidity', 'soil_moisture')
    list_filter = ('timestamp', 'field')
