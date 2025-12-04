from django.contrib import admin
from .models import Crop, CropCycle, RecommendationLog, YieldLog, DiseaseLog

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'variety', 'min_temp', 'max_temp')
    search_fields = ('name', 'variety')

@admin.register(CropCycle)
class CropCycleAdmin(admin.ModelAdmin):
    list_display = ('crop', 'field', 'planting_date', 'harvest_date', 'is_active')
    list_filter = ('is_active', 'planting_date', 'crop')

@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommended_crop', 'confidence', 'created_at')
    list_filter = ('recommended_crop', 'created_at')
    search_fields = ('user__username', 'recommended_crop')
    readonly_fields = ('created_at',)

@admin.register(YieldLog)
class YieldLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'crop_name', 'area', 'predicted_yield', 'created_at')
    list_filter = ('crop_name', 'created_at')
    search_fields = ('user__username', 'crop_name')
    readonly_fields = ('created_at',)

@admin.register(DiseaseLog)
class DiseaseLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_disease', 'confidence', 'created_at')
    list_filter = ('predicted_disease', 'created_at')
    search_fields = ('user__username', 'predicted_disease')
    readonly_fields = ('created_at',)
