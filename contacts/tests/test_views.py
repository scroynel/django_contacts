import pytest

from django.urls import reverse


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