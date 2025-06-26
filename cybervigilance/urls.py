from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_cybervigilance_view, name='test_cybervigilance'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
