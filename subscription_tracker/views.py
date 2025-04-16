# from django.shortcuts import render
from django.http import HttpResponse


def hello_message(request):
    return HttpResponse("Hello, this is Subscription Tracker!")
