from django.shortcuts import render
from django.http import HttpResponse, Http404


def detail_view(request):
    return render(request, 'detail/index.html')


def index(request, detail_id):
    try:
        value = detail_view.object.get(id=detail_id)
    except:
        raise Http404('Страница отсутствует, с id: ' + str(detail_id))
    return render(request, 'detail/index.html', {'detail': value})
