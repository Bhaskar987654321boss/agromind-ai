from django.db import models
from django.conf import settings
from farms.models import Field

class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    variety = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    min_temp = models.FloatField(help_text="Minimum optimal temperature")
    max_temp = models.FloatField(help_text="Maximum optimal temperature")
    min_rainfall = models.FloatField(help_text="Minimum rainfall required (mm)")
    max_rainfall = models.FloatField(help_text="Maximum rainfall required (mm)")
    
    def __str__(self):
        return f"{self.name} - {self.variety}" if self.variety else self.name

class CropCycle(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='crop_cycles')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    planting_date = models.DateField()
    harvest_date = models.DateField(blank=True, null=True)
    estimated_yield = models.FloatField(help_text="Estimated yield in quintals", blank=True, null=True)
    actual_yield = models.FloatField(help_text="Actual yield in quintals", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.crop.name} on {self.field.name} ({self.planting_date})"

class RecommendationLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    soil_moisture = models.CharField(max_length=50, blank=True, null=True)
    recommended_crop = models.CharField(max_length=100)
    confidence = models.FloatField(default=0.0)

    def __str__(self):
        return f"Recommendation for {self.user} at {self.created_at}"

class YieldLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    crop_name = models.CharField(max_length=100)
    area = models.FloatField()
    soil_type = models.CharField(max_length=50)
    rainfall = models.FloatField()
    temperature = models.FloatField()
    fertilizer = models.FloatField(default=0)
    irrigation = models.CharField(max_length=50, default='None')
    predicted_yield = models.FloatField()

    def __str__(self):
        return f"Yield Prediction for {self.user} at {self.created_at}"

class DiseaseLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    crop_name = models.CharField(max_length=100, blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    predicted_disease = models.CharField(max_length=100)
    confidence = models.FloatField(default=0.0)

    def __str__(self):
        return f"Disease Detection for {self.user} at {self.created_at}"
