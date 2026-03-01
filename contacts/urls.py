from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import ContactListView, ContactCreateView, ContactUpdateView, ContactDeleteView, MyLoginView


urlpatterns = [
    path('', ContactListView.as_view(), name='contacts'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-contact/', ContactCreateView.as_view(), name='create_contact'),
    path('update-contact/<int:pk>/', ContactUpdateView.as_view(), name='update_contact'),
    path('delete-contact/<int:pk>/', ContactDeleteView.as_view(), name='delete_contact')
]