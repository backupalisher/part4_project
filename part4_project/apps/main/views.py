from django.shortcuts import render
from django.db import connections
from django.core import serializers
import db_model.models as models

def index(request):
    brands = models.Brands.objects.all().order_by('name')
    return render(request, 'main/index.html', context={'search_block': True, 'brands': brands})


def search(request):
    s_value = request.GET.__getitem__('s')
    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.callproc('details_search_v2', (s_value,))
            r = c.fetchall()
            c.execute("COMMIT")
            return render(request, 'main/index.html', context={'sresult': r})
        finally:
            c.close()
