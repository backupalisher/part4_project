from django.shortcuts import render


def model(request):
    return render(request, 'model/index.html')