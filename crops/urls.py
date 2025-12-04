from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.recommend_crop, name='recommend_crop'),
    path('recommend/pdf/', views.download_recommendation_pdf, name='download_recommendation_pdf'),
    path('yield/', views.predict_yield, name='predict_yield'),
    path('yield/pdf/', views.download_yield_pdf, name='download_yield_pdf'),
    path('disease/', views.detect_disease, name='detect_disease'),
    path('disease/pdf/', views.download_disease_pdf, name='download_disease_pdf'),
]
