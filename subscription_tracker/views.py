from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets
from .models import Subscription
from subscription_tracker.api.serializers import SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal


def hello_message(request):
    return HttpResponse("Hello, this is Subscription Tracker!")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("hello")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="tracker/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("hello")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="tracker/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("hello")


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@login_required
def monthly_expenses(request):
    user = request.user
    subscriptions = Subscription.objects.filter(user=user)

    monthly_total = Decimal('0.00')

    for sub in subscriptions:
        if sub.frequency == 'monthly':
            monthly_total += sub.price
        elif sub.frequency == 'yearly':
            monthly_total += sub.price / Decimal('12')
        elif sub.frequency == 'weekly':
            monthly_total += sub.price * Decimal('4.33')
        elif sub.frequency == 'daily':
            monthly_total += sub.price * Decimal('30')

    return JsonResponse({
        'monthly_expense': round(monthly_total, 2),
        'currency': 'USD'
    })
