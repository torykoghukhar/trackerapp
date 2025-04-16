import pytest
from django.contrib.auth.models import User
from .models import Subscription
from datetime import date


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
