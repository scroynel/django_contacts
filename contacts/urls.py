from django.urls import path
from .views import contacts
from .autocomplete_view import CityAutocomplete


urlpatterns = [
    path('', contacts, name='contacts'),
    path(
        'city-autocomplete/',
        CityAutocomplete.as_view(),
        name='city-autocomplete'
    ),
]