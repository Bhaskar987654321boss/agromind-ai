from django.core.management.base import BaseCommand
from crops.models import Crop

class Command(BaseCommand):
    help = 'Populates the database with a comprehensive list of crops'

    def handle(self, *args, **kwargs):
        crops_data = [
            # Cereals
            {"name": "Rice", "min_temp": 20, "max_temp": 35, "min_rain": 100, "max_rain": 200},
            {"name": "Wheat", "min_temp": 10, "max_temp": 25, "min_rain": 40, "max_rain": 100},
            {"name": "Maize", "min_temp": 18, "max_temp": 30, "min_rain": 50, "max_rain": 100},
            {"name": "Barley", "min_temp": 10, "max_temp": 25, "min_rain": 30, "max_rain": 90},
            {"name": "Millet", "min_temp": 20, "max_temp": 35, "min_rain": 30, "max_rain": 70},
            
            # Pulses
            {"name": "Chickpea", "min_temp": 15, "max_temp": 25, "min_rain": 30, "max_rain": 60},
            {"name": "Pigeonpea", "min_temp": 20, "max_temp": 35, "min_rain": 50, "max_rain": 100},
            {"name": "Mungbean", "min_temp": 25, "max_temp": 35, "min_rain": 40, "max_rain": 80},
            {"name": "Blackgram", "min_temp": 25, "max_temp": 35, "min_rain": 40, "max_rain": 80},
            {"name": "Lentil", "min_temp": 10, "max_temp": 25, "min_rain": 30, "max_rain": 60},
            
            # Cash Crops
            {"name": "Cotton", "min_temp": 20, "max_temp": 30, "min_rain": 50, "max_rain": 100},
            {"name": "Jute", "min_temp": 25, "max_temp": 35, "min_rain": 150, "max_rain": 250},
            {"name": "Sugarcane", "min_temp": 20, "max_temp": 35, "min_rain": 100, "max_rain": 200},
            {"name": "Tobacco", "min_temp": 20, "max_temp": 30, "min_rain": 50, "max_rain": 100},
            
            # Oilseeds
            {"name": "Groundnut", "min_temp": 20, "max_temp": 30, "min_rain": 50, "max_rain": 100},
            {"name": "Mustard", "min_temp": 10, "max_temp": 25, "min_rain": 20, "max_rain": 50},
            {"name": "Soybean", "min_temp": 20, "max_temp": 35, "min_rain": 50, "max_rain": 100},
            {"name": "Sunflower", "min_temp": 20, "max_temp": 30, "min_rain": 30, "max_rain": 80},
            
            # Fruits/Veg
            {"name": "Potato", "min_temp": 15, "max_temp": 25, "min_rain": 50, "max_rain": 100},
            {"name": "Onion", "min_temp": 15, "max_temp": 30, "min_rain": 50, "max_rain": 100},
            {"name": "Tomato", "min_temp": 15, "max_temp": 30, "min_rain": 50, "max_rain": 100},
            {"name": "Brinjal", "min_temp": 20, "max_temp": 35, "min_rain": 50, "max_rain": 100},
            {"name": "Chilli", "min_temp": 20, "max_temp": 35, "min_rain": 50, "max_rain": 100},
            {"name": "Tea", "min_temp": 15, "max_temp": 30, "min_rain": 150, "max_rain": 300},
            {"name": "Coffee", "min_temp": 15, "max_temp": 28, "min_rain": 150, "max_rain": 250},
            {"name": "Banana", "min_temp": 20, "max_temp": 35, "min_rain": 100, "max_rain": 250},
            {"name": "Mango", "min_temp": 20, "max_temp": 35, "min_rain": 50, "max_rain": 150},
            {"name": "Grapes", "min_temp": 15, "max_temp": 35, "min_rain": 50, "max_rain": 100},
            {"name": "Apple", "min_temp": 5, "max_temp": 25, "min_rain": 50, "max_rain": 100},
            {"name": "Orange", "min_temp": 15, "max_temp": 35, "min_rain": 50, "max_rain": 150},
            {"name": "Papaya", "min_temp": 20, "max_temp": 35, "min_rain": 100, "max_rain": 200},
            {"name": "Coconut", "min_temp": 20, "max_temp": 35, "min_rain": 100, "max_rain": 250},
        ]

        for data in crops_data:
            crop, created = Crop.objects.get_or_create(
                name=data['name'],
                defaults={
                    'min_temp': data['min_temp'],
                    'max_temp': data['max_temp'],
                    'min_rainfall': data['min_rain'],
                    'max_rainfall': data['max_rain'],
                    'description': f"Standard {data['name']} crop."
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created crop: {crop.name}"))
            else:
                self.stdout.write(f"Crop already exists: {crop.name}")

        self.stdout.write(self.style.SUCCESS('Successfully populated crops'))
