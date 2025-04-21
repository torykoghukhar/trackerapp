import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from subscription_tracker.models import Subscription
from datetime import date
from rest_framework.reverse import reverse


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def subscription(user):
    return Subscription.objects.create(
        user=user,
        name='Netflix',
        price=9.99,
        frequency='monthly',
        next_billing_date=date(2025, 5, 1)
    )


@pytest.mark.django_db
def test_get_list(client, subscription):
    url = reverse('subscription-list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['results'][0]['name'] == 'Netflix'


@pytest.mark.django_db
def test_create_subscription(client):
    url = reverse('subscription-list')
    data = {
        "name": "Spotify",
        "price": 4.99,
        "frequency": "monthly",
        "next_billing_date": "2025-06-01"
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.data['name'] == 'Spotify'


@pytest.mark.django_db
def test_update_subscription(client, subscription):
    url = reverse('subscription-detail', args=[subscription.id])
    data = {
        "name": "Netflix HD",
        "price": 11.99,
        "frequency": "monthly",
        "next_billing_date": "2025-05-01"
    }
    response = client.put(url, data)
    assert response.status_code == 200
    assert response.data['name'] == 'Netflix HD'


@pytest.mark.django_db
def test_partial_update(client, subscription):
    url = reverse('subscription-detail', args=[subscription.id])
    data = {"price": 12.99}
    response = client.patch(url, data)
    assert response.status_code == 200
    assert response.data['price'] == '12.99'


@pytest.mark.django_db
def test_delete_subscription(client, subscription):
    url = reverse('subscription-detail', args=[subscription.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert Subscription.objects.count() == 0
