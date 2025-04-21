from celery import shared_task
from django.core.mail import send_mail
from datetime import date, timedelta
from .models import Subscription


@shared_task
def send_billing_alerts():
    tomorrow = date.today() + timedelta(days=1)
    subscriptions = Subscription.objects.filter(next_billing_date=tomorrow)

    for sub in subscriptions:
        user_email = sub.user.email
        if user_email:
            send_mail(
                subject='Subscription payment reminder',
                message=f'Hello! We would like to remind you that tomorrow ({
                    sub.next_billing_date}) there will be a charge for the subscription: {
                    sub.name} ({
                    sub.price}$)',
                from_email=None,
                recipient_list=[user_email],
                fail_silently=False,
            )


@shared_task
def send_test_email():
    send_mail(
        'Test Email',
        'This is a test email sent via Celery.',
        'vika.koghukhar@gmail.com',
        ['vika.koghukhar@gmail.com'],
        fail_silently=False,
    )
