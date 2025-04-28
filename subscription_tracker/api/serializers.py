from rest_framework import serializers
from subscription_tracker.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'name',
            'price',
            'frequency',
            'next_billing_date',
        ]
        read_only_fields = ['id', 'user']
