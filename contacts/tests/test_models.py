import pytest
from contacts.models import Contact, ContactStatusChoices, GeoCache
from django.contrib.auth.models import User

from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError


# @pytest.fixture
# def test_user(db):
#     user = User.objects.create_user(username="testuser", password='testpassword')
#     return user


# @pytest.fixture
# def test_status(db):
#     status = ContactStatusChoices.objects.create(name='Nowy', code='new')
#     return status


# @pytest.fixture
# def test_contact(db, test_user, test_status):
#     contact = Contact.objects.create(
#         name='Piter',
#         surname='Parker',
#         phone = '+48798498754',
#         email = 'piterpark@gmail.com',
#         city = 'Warsaw',
#         status=test_status,
#         owner=test_user
#     )
#     return contact


# @pytest.fixture
# def test_geocache(db):
#     geocache = GeoCache.objects.create(city_name='Warsaw', lat=52.22, lon=21.01)
#     return geocache





@pytest.mark.django_db
def test_contact_str_representation(test_contact):
    assert str(test_contact) == 'Piter - Parker - Nowy'


@pytest.mark.django_db
def test_status_str_representation(test_status):
    assert str(test_status) == 'Nowy'


@pytest.mark.django_db
def test_geocache_str_representation(test_geocache):
    assert str(test_geocache) == 'Warsaw'


@pytest.mark.django_db
def test_owner_cascade_delete(test_user):
    test_user.delete()
    assert Contact.objects.count() == 0


@pytest.mark.django_db
def test_owner_protect_delete(test_contact):
    with pytest.raises(ProtectedError):
        test_contact.status.delete()
    
# One function runs 4 times for every parametr we updated instead of 4 different functions (DRY)    
@pytest.mark.django_db
@pytest.mark.parametrize('invalid_data', [
    {'email': None},                    # Missing email
    {'phone': None},                    # Missing phone
    {'email': 'piterpark@gmail.com'},   # Dublicate email
    {'phone': '+48798498754'}           # Dublicate phone
])
def test_contact_constraints(test_contact, test_user, test_status, invalid_data):
    
    data = {
        'name': 'John',
        'surname': 'Smith',
        'phone': '+48753598754',
        'email': 'john_smith@gmail.com',
        'city': 'Gdansk',
        'status': test_status,
        'owner': test_user
    }

    data.update(invalid_data)

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Contact.objects.create(**data)
            

@pytest.mark.django_db
def test_geocache_unique():
    GeoCache.objects.create(city_name='Warsaw', lat=52.22, lon=21.01)

    with pytest.raises(IntegrityError):
        GeoCache.objects.create(city_name='Warsaw', lat=0.0, lon=0.0)