from django.db import models
from django.conf import settings
from crops.models import Crop

class MarketPrice(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='market_prices')
    market_name = models.CharField(max_length=100)
    date = models.DateField()
    price_per_quintal = models.FloatField()
    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.crop.name} at {self.market_name} on {self.date}: {self.price_per_quintal}"

class SaleListing(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity_kg = models.FloatField()
    price_per_kg = models.FloatField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.crop.name} by {self.seller.username} - {self.quantity_kg}kg"
