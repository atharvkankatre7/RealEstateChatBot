"""
URL configuration for API endpoints
"""
from django.urls import path
from . import views

urlpatterns = [
    path('query/', views.query_analysis, name='query_analysis'),
    path('localities/', views.get_localities, name='get_localities'),
    path('health/', views.health_check, name='health_check'),
    path('download/', views.download_data, name='download_data'),
]
