from django.contrib import admin
from .models import MarketPrice, SaleListing

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ('crop', 'market_name', 'date', 'price_per_quintal')
    list_filter = ('market_name', 'crop', 'date')

@admin.register(SaleListing)
class SaleListingAdmin(admin.ModelAdmin):
    list_display = ('seller', 'crop', 'quantity_kg', 'price_per_kg', 'is_sold', 'created_at')
    list_filter = ('is_sold', 'crop')
