from django.shortcuts import render
from .services import send


# Create your views here.
def index(request):
    success_url = '/'
    send(request)

    return render(request, '/')
