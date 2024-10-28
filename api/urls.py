# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('groupes/', views.liste_groupes, name='liste_groupes'),
    path('groupes/<uuid:pk>/', views.details_groupe, name='details_groupe'),
    path('gardiens/', views.liste_gardiens, name='liste_gardiens'),
    path('gardiens/<uuid:pk>/', views.details_gardien, name='details_gardien'),
    path('groupes/<uuid:groupe_id>/toggle/', views.toggle_groupe_etat, name='toggle_groupe_etat'),
    path('groupes/enregistrer_gardien/', views.enregistrer_gardien, name='enregistrer_gardien'),
    path('logs/', views.logs_par_jour, name='logs_par_jour'),
    path('temps-utilisation/<uuid:groupe_uuid>/', views.obtenir_temps_utilisation, name='obtenir_temps_utilisation'),
    path('bilan-groupes/', views.bilan_groupes, name='bilan_groupes'),
    path('groupes/marques/', views.get_group_brands, name='get_group_brands')
]
