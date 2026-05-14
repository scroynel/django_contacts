import pytest
from unittest.mock import patch

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from contacts.models import Contact


# Test MyLoginView
@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)

    assert response.status_code == 200 
    assert 'contacts/registration/login.html' in [i.name for i in response.templates]
   

@pytest.mark.django_db
def test_login_success(client, test_user):
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'testpassword'
    })

    print(test_user.username) # i need to change it for the data in response

    assert response.status_code == 302 # redirect after login
    assert response.url == reverse('contacts')


# Test ContactListView
@pytest.mark.django_db
def test_contact_list_view_if_not_logged_in(client):
    url = reverse('contacts')
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_contact_list_view_filtered_by_owner(auth_client, test_user):
    url = reverse('contacts')
    response = auth_client.get(url)

    contacts = response.context['contacts']
    
    assert all(contact.owner.username == test_user.username for contact in contacts)


@pytest.mark.django_db
def test_contact_list_view_csv_upload(auth_client, test_user, test_status):
    csv_data = (
        'name,surname,phone,email,city,status\n'
        'John,Olsson,+48736837848,jognol@gmail.com,Opole,Nowy\n'
    )

    file = SimpleUploadedFile('contacts.csv', csv_data.encode('utf-8'), content_type='text/csv')
    url = reverse('contacts')

    response = auth_client.post(url, {'file': file})

    assert response.status_code == 302
    assert Contact.objects.filter(owner=test_user).count() == 1


@pytest.mark.django_db
def test_contact_list_view_csv_upload_skips_dublicates(auth_client, test_user, test_contact):
    csv_data = (
        'name,surname,phone,email,city,status\n'
        'John,Olsson,+48798498754,jognol@gmail.com,Opole,Nowy\n' # phone dublicate
    )

    file = SimpleUploadedFile('contacts.csv', csv_data.encode('utf-8'),  content_type='text/csv')
    url = reverse('contacts')

    response = auth_client.post(url, {'file': file})

    assert Contact.objects.filter(owner=test_user).count() == 1


@patch("contacts.views.fetch_coords_background")
@patch("contacts.views.fetch_weather_by_coords", return_value=[])
def test_view_with_weather_mock(mock_weather, mock_bg, auth_client, test_user, test_status, test_contact):
    url = reverse('contacts')
    response = auth_client.get(url)

    assert response.status_code == 200
    mock_weather.assert_called()


@pytest.mark.django_db
def test_contact_create_view_if_not_logged_in(client):
    url = reverse('create_contact')
    response = client.get(url)
    
    assert response.status_code == 302
    assert '/login/' in response.url


@pytest.mark.django_db
def test_contact_create_view_create_contact(auth_client, contact_data, test_user):
    url = reverse('create_contact')

    with patch("contacts.views.fetch_coords_background") as mock_task:
        response = auth_client.post(url, contact_data)

    assert response.status_code == 302
    assert response.url == reverse('contacts')

    contact = Contact.objects.get(email='piterpark@gmail.com')

    assert contact.name == 'Piter'
    assert contact.city == 'Gdansk'
    assert contact.owner == test_user

    mock_task.assert_called_once_with('Gdansk')


@pytest.mark.django_db
def test_contact_create_view_invalid_form(auth_client, contact_data):
    url = reverse('create_contact')
    data = contact_data
    data['name'] = ''
    
    response = auth_client.post(url, contact_data)

    assert response.status_code == 200
    assert Contact.objects.count() == 0


@pytest.mark.django_db
def test_contact_update_view_update_own_contact(auth_client, test_contact):
    url = reverse('update_contact', args=[test_contact.id])
    contact = test_contact
    response = auth_client.post(url, {
        'name': 'Tomas',
        'surname': test_contact.surname,
        'phone': test_contact.phone,
        'email': test_contact.email,
        'city': test_contact.city,
        'status': test_contact.status.id
    })

    contact.refresh_from_db()

    assert response.status_code == 302
    assert contact.name == 'Tomas'


@pytest.mark.django_db
def test_contact_update_view_update_someone_contact(auth_client, test_contact2):
    url = reverse('update_contact', args=[test_contact2.id])
    contact = test_contact2
    response = auth_client.get(url)

    assert response.status_code == 404



@patch("contacts.views.fetch_coords_background")
def test_contact_update_view_city_changed(mock_fetch_coords, auth_client, test_contact):
    url = reverse('update_contact', args=[test_contact.id])
    response = auth_client.post(url, {
        'name': test_contact.name,
        'surname': test_contact.surname,
        'phone': test_contact.phone,
        'email': test_contact.email,
        'city': 'Gdansk',
        'status': test_contact.status.id
    })

    mock_fetch_coords.assert_called_once_with('Gdansk')



@patch("contacts.views.fetch_coords_background")
def test_contact_update_view_city_not_changed(mock_fetch_coords, auth_client, test_contact):
    url = reverse('update_contact', args=[test_contact.id])
    response = auth_client.post(url, {
        'name': 'Tom',
        'surname': test_contact.surname,
        'phone': test_contact.phone,
        'email': test_contact.email,
        'city': 'Warsaw',
        'status': test_contact.status.id
    })

    mock_fetch_coords.assert_not_called()

@pytest.mark.django_db
def test_ajax_request_delete_contact(auth_client, test_contact):
    url = reverse('delete_contact', args=[test_contact.id])
    response = auth_client.post(url, HTTP_X_REQUESTED_WITH= 'XMLHttpRequest')

    assert response.status_code == 200
    assert response.json() == {'status': 1}
    assert Contact.objects.filter(id=test_contact.id).count() == 0


@pytest.mark.django_db
def test_non_ajax_request(auth_client, test_contact):
    url = reverse('delete_contact', args=[test_contact.id])
    response = auth_client.post(url)

    assert response.status_code == 400

@pytest.mark.django_db
def test_ajax_delete_unauthenticated_user_redirect(client, test_contact):
    url = reverse('delete_contact', args=[test_contact.id])
    response = client.post(url, HTTP_X_REQUESTED_WITH= 'XMLHttpRequest')

    assert response.status_code == 302


@pytest.mark.django_db
def test_ajax_delete_other_user_contact(auth_client, test_contact2):
    url = reverse('delete_contact', args=[test_contact2.id])
    response = auth_client.post(url, HTTP_X_REQUESTED_WITH= 'XMLHttpRequest')

    assert response.status_code == 404