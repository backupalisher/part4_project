from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


# Create your views here.
def index(request):
    title = 'Фильтр'
    return render(request, 'filter/index.html', {'title': title})
