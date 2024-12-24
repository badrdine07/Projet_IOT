from django.urls import path
from .views import Dlist, Dhtviews, DlistByDateRange, DlistByPeriod  # Assurez-vous d'importer DlistByPeriod

urlpatterns = [
    path('dht11/get/', Dlist, name='dht11-get'),  # Pour afficher la liste des données (GET)
    path('dht11/post/', Dhtviews.as_view(), name='dht11-post'),  # Pour créer une nouvelle entrée (POST)
    path('dht11/get/by-period/', DlistByPeriod, name='dht11-get-by-period'),  # Pour obtenir des données par période
        path('dht11/get/by-date-range/', DlistByDateRange, name='dht11-get-by-date-range'),  # Pour obtenir des données par date

]
