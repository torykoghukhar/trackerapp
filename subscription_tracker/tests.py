import pytest
from django.contrib.auth.models import User
from .models import Subscription
from datetime import date
from django.urls import reverse
from django.contrib.messages import get_messages


@pytest.mark.django_db
def test_create_subscription():
    user = User.objects.create_user(username='testuser', password='testpass')
    sub = Subscription.objects.create(
        user=user,
        name='Netflix',
        price=9.99,
        frequency='monthly',
        next_billing_date=date(2025, 5, 1)
    )
    assert sub.name == 'Netflix'
    assert sub.frequency == 'monthly'
    assert str(sub) == 'Netflix (monthly)'


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', email='test@example.com', password='password123')


@pytest.mark.django_db
def test_register_valid_data(client):
    url = reverse('register')
    response = client.post(url, {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'Strongpass123',
        'password2': 'Strongpass123',
    })
    assert response.status_code == 302  # Redirect to "hello"
    assert User.objects.filter(username='newuser').exists()

    follow_response = client.get(reverse('hello'))
    messages = list(get_messages(follow_response.wsgi_request))
    assert any("Registration successful" in str(m) for m in messages)


@pytest.mark.django_db
def test_register_invalid_data(client):
    url = reverse('register')
    response = client.post(url, {
        'username': '',
        'email': 'bademail',
        'password1': '123',
        'password2': '456',
    })
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert any("Unsuccessful registration" in str(m) for m in messages)


@pytest.mark.django_db
def test_login_valid_credentials(client, test_user):
    url = reverse('login')
    response = client.post(url, {
        'username': 'testuser',
        'password': 'password123',
    })
    assert response.status_code == 302

    follow_response = client.get(reverse('hello'))
    messages = list(get_messages(follow_response.wsgi_request))
    assert any("You are now logged in as testuser." in str(m) for m in messages)


@pytest.mark.django_db
def test_login_invalid_credentials(client):
    url = reverse('login')
    response = client.post(url, {
        'username': 'wronguser',
        'password': 'wrongpass',
    })
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert any("Invalid username or password" in str(m) for m in messages)


@pytest.mark.django_db
def test_logout(client, test_user):
    client.login(username='testuser', password='password123')
    url = reverse('logout')
    response = client.get(url)

    assert response.status_code == 302
    follow_response = client.get(reverse('hello'))
    messages = list(get_messages(follow_response.wsgi_request))
    assert any("You have successfully logged out." in str(m) for m in messages)
