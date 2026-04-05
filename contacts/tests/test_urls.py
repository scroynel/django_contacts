import pytest
from django.urls import reverse, resolve
from contacts.views import ContactListView
from django.contrib.auth.models import User

from contacts.models import Contact

from unittest.mock import patch


@pytest.mark.django_db
@pytest.mark.parametrize('url_name,args', [
    ('contacts', []),
    ('create_contact', []),
    ('update_contact', [1]),
    ('delete_contact', [1])
])
def test_required_login(client, test_contact, url_name, args):
    if args:
        args[0] = test_contact.id
    url_path = reverse(url_name, args=args)
    response = client.get(url_path)

    assert response.status_code == 302
    assert '/login/' in response.url


# Using mock that return data, because there was an error JSONDecodeError
@patch("contacts.views.fetch_weather_by_coords")
def test_contacts_page(mock_weather, client, test_user, test_contact):
    mock_weather.return_value([
        {"temp": "20 °C", "wind": "5 km/h"}
    ])

    client.force_login(test_user)
    url_path = reverse('contacts')
    response = client.get(url_path)

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url_name,args', [
    ('create_contact', []),
    ('update_contact', [1])
])
def test_with_login(client, test_contact, test_user, url_name, args):
    client.force_login(test_user)

    if args:
        args[0] = test_contact.id

    url_path = reverse(url_name, args=args)
    response = client.get(url_path)
    assert response.status_code == 200


# Write the same test and check the data assert test_contact.city == 'Gdansk' ...
@pytest.mark.django_db
def test_update_contact_status(client, test_user, test_contact, test_status):
    client.force_login(test_user)
    url_path = reverse('update_contact', args=[test_contact.id])
    
    data = {
        'name': 'Piter',
        'surname': 'Walker',
        'phone': '+48798498754',
        'email': 'piterpark@gmail.com',
        'city': 'Gdansk',
        'status': test_status.id
    }

    response = client.post(url_path, data)

    assert response.status_code == 302
    assert response.url == reverse('contacts')


@pytest.mark.django_db
def test_delete_contact_status_ajax(client, test_user, test_contact):
    client.force_login(test_user)
    url_path = reverse('delete_contact', args=[test_contact.id])
    response = client.post(url_path, HTTP_X_REQUESTED_WITH='XMLHttpRequest') # For AJAX request

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_contact_exists(client, test_user, test_contact):
    client.force_login(test_user)
    url_path = reverse('delete_contact', args=[test_contact.id])
    response = client.post(url_path, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    assert not Contact.objects.filter(id=test_contact.id).exists()




    

# @pytest.mark.django_db
# @pytest.mark.parametrize('url_name', [
#     'login',
#     'api_contacts-list'
# ])
# def test_public_pages(client, url_name):
#     url_path = reverse(url_name)
#     response = client.get(url_path)
    
#     assert response.status_code == 200