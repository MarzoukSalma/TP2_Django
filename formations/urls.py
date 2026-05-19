from django.urls import path
from . import views

urlpatterns = [
    # URLs normales
    path('', views.liste_formations, name='liste_formations'),
    path('ajouter/', views.ajouter_formation, name='ajouter_formation'),
    path('modifier/<int:pk>/', views.modifier_formation, name='modifier_formation'),
    path('supprimer/<int:pk>/', views.supprimer_formation, name='supprimer_formation'),

    # URLs API
    path('api/', views.api_liste_formations, name='api_liste'),
    path('api/ajouter/', views.api_ajouter_formation, name='api_ajouter'),
    path('api/<int:pk>/', views.api_formation_detail, name='api_detail'),
]