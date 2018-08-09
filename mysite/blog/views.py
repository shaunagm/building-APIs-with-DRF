from django.shortcuts import render
from django.http import HttpResponse


def Index(request):
    return HttpResponse("This is the regular ol' index page for our blog app.")
