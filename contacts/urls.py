from django.urls import path
from .views import contacts, ContactListView
from .autocomplete_view import CityAutocomplete


urlpatterns = [
    path('', ContactListView.as_view(), name='contacts'),
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete'),
]