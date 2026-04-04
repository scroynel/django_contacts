import pytest
from django.urls import reverse, resolve
from contacts.views import ContactListView
from django.contrib.auth.models import User

from unittest.mock import patch



# @pytest.mark.django_db
# def test_contacts_url(client):
#     # user = User.objects.create_user(username='testuser', password='password')
#     # client.login(username='testuser', password='password')

#     url_path = reverse('contacts')

#     assert url_path == '/'

#     print('resolve', resolve(url_path))

#     response = client.get(url_path)

#     print(response)

#     assert response.status_code == 200


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


@patch("contacts.views.fetch_weather_by_coords")
def test_contacts_page(mock_weather, client, test_user, test_contact):
    mock_weather.return_value([
        {"temp": "20 °C", "wind": "5 km/h"}
    ])

    client.force_login(test_user)
    url_path = reverse('contacts')
    response = client.get(url_path)

    assert response.status_code == 200



# @pytest.mark.django_db
# @pytest.mark.parametrize('url_name,args', [
#     ('contacts', []),
#     ('create_contact', []),
#     ('update_contact', [1])
# ])
# def test_with_login(client, test_contact, test_user, url_name, args):
#     client.force_login(test_user)

#     if args:
#         args[0] = test_contact.id

#     url_path = reverse(url_name, args=args)
#     response = client.get(url_path)
#     assert response.status_code == 200



# @pytest.mark.django_db
# @pytest.mark.parametrize('url_name', [
#     'login',
#     'api_contacts-list'
# ])
# def test_public_pages(client, url_name):
#     url_path = reverse(url_name)
#     response = client.get(url_path)
    
#     assert response.status_code == 200