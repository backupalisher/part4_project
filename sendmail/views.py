from django.http import HttpResponse
from django.shortcuts import render
from .services import send, send_contact


# Create your views here.
def index(request):
    print(request)
    send(request)

    return render(request, '/')


def contact(request):
    url = request.POST['url']
    print(url)
    send_contact(request)

    return HttpResponse('successful')
