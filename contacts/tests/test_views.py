import pytest

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
def test_contact_list_view_if_not_logged_id(client):
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

    responser = auth_client.post(url, {'file': file})

    assert Contact.objects.filter(owner=test_user).count() == 1