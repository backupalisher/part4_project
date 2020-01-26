from django.shortcuts import render
from django.db import connections
from django.core import serializers


def index(request):
    return render(request, 'main/index.html', context={'search_block': True})


def search(request):
    s_value = request.GET.__getitem__('s')
    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.callproc('details_search_v2', (s_value,))
            r = c.fetchall()
            c.execute("COMMIT")
            print(r)
            return render(request, 'main/index.html', context={'sresult': r})
        finally:
            c.close()
