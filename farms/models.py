from django.db import models
from django.conf import settings

class Field(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=100)
    area_hectares = models.FloatField(help_text="Area in hectares")
    location_lat = models.FloatField(blank=True, null=True)
    location_lon = models.FloatField(blank=True, null=True)
    soil_type = models.CharField(max_length=100, help_text="e.g., Alluvial, Black, Red, etc.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

class SensorLog(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='sensor_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField(help_text="Temperature in Celsius")
    humidity = models.FloatField(help_text="Humidity in %")
    soil_moisture = models.FloatField(help_text="Soil Moisture in %")

    def __str__(self):
        return f"Log for {self.field.name} at {self.timestamp}"
