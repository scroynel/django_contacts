import pytest
import json
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
def test_update_contact_status(auth_client, update_contact_url, contact_data):
    response = auth_client.post(update_contact_url, data=contact_data)

    assert response.status_code == 302
    assert response.url == reverse('contacts')


@pytest.mark.django_db
def test_update_contact_check_data(auth_client, update_contact_url, contact_data, test_contact):
    auth_client.post(update_contact_url, data=contact_data)
    test_contact.refresh_from_db()

    assert test_contact.name == 'Piter'
    assert test_contact.surname == 'Walker'
    assert test_contact.city == 'Gdansk'
    

@pytest.mark.django_db
def test_delete_contact_status_ajax(auth_client, delete_contact_url, ajax_headers):
    response = auth_client.post(delete_contact_url, **ajax_headers) # For AJAX request

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_contact_exists(auth_client, delete_contact_url, ajax_headers, test_contact):
    auth_client.post(delete_contact_url, **ajax_headers)

    assert not Contact.objects.filter(id=test_contact.id).exists()


@pytest.mark.django_db
@pytest.mark.parametrize('url_name', [
    'login',
    'api_contacts-list'
])
def test_public_pages(client, url_name):
    url_path = reverse(url_name)
    response = client.get(url_path)
    
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_contact_create(auth_client, test_user, test_status):
    response = auth_client.post('/api/contacts/', data=json.dumps(
        {
            'name': 'John',
            'surname': 'Olsson',
            'phone': '+48458498766',
            'email': 'johnolss@gmail.com',
            'city': 'Warsaw',
            'status': test_status.id,
            'owner': test_user.id
        }), 
        content_type='application/json'
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_api_contact_update(auth_client, test_contact, test_status, test_user):
    response = auth_client.put(f'/api/contacts/{test_contact.id}/', data=json.dumps(
        {
            'name': 'John',
            'surname': 'Smith',
            'phone': '+48458498766',
            'email': 'johnolss@gmail.com',
            'city': 'Warsaw',
            'status': test_status.id,
            'owner': test_user.id
        }),
        content_type='application/json'
    )

    test_contact.refresh_from_db()

    assert response.status_code == 200
    assert test_contact.email == 'johnolss@gmail.com'
    assert test_contact.surname == 'Smith'


@pytest.mark.django_db
def test_api_contact_delete(auth_client, test_contact):
    response = auth_client.delete(f'/api/contacts/{test_contact.id}/')

    assert response.status_code == 204
    assert not Contact.objects.filter(id=test_contact.id).exists()