from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.hello_message, name='hello'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("api/", include('subscription_tracker.api.urls')),
]
