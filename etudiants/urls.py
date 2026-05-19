from django.urls import path
from . import views

urlpatterns = [
    path('inscrire/<int:pk>/', views.inscrire, name='inscrire'),
]