from django.urls import reverse
from django.contrib.auth import get_user_model

import pytest
from contacts.models import Contact, ContactStatusChoices, GeoCache

User = get_user_model()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username="testuser", password='testpassword')
    return user


@pytest.fixture
def test_status(db):
    status = ContactStatusChoices.objects.create(name='Nowy', code='new')
    return status


@pytest.fixture
def test_contact(db, test_user, test_status):
    contact = Contact.objects.create(
        name='Piter',
        surname='Parker',
        phone = '+48798498754',
        email = 'piterpark@gmail.com',
        city = 'Warsaw',
        status=test_status,
        owner=test_user
    )
    return contact


@pytest.fixture
def test_geocache(db):
    geocache = GeoCache.objects.create(city_name='Warsaw', lat=52.22, lon=21.01)
    return geocache


@pytest.fixture
def auth_client(client, test_user):
    client.force_login(test_user)
    return client


@pytest.fixture
def delete_contact_url(test_contact):
    return reverse('delete_contact', args=[test_contact.id])


@pytest.fixture
def ajax_headers():
    return {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}


@pytest.fixture
def update_contact_url(test_contact):
    return reverse('update_contact', args=[test_contact.id])


@pytest.fixture
def contact_data(test_status):
    return {
        'name': 'Piter',
        'surname': 'Walker',
        'phone': '+48798498754',
        'email': 'piterpark@gmail.com',
        'city': 'Gdansk',
        'status': test_status.id
    }