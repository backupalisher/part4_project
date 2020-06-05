import datetime

from django.shortcuts import render
from django.db import connections
from django.core import serializers
import db_model.models as models
start_time = datetime.datetime.now()


def index(request):
    brands = models.Brands.objects.all()
    return render(request, 'main/index.html', context={'search_block': True, 'brands': brands})


def search(request):
    variant = int(request.GET.__getitem__('v'))
    s_value = request.GET.__getitem__('s')
    ar = None
    er = None
    cr = None
    if variant:
        pass
    else:
        variant = 0
    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            if variant == 0:
                c.callproc('details_search_v1', (s_value,))
                ar = c.fetchall()
            elif variant == 1:
                c.callproc('error_search', (s_value,))
                er = c.fetchall()
            elif variant == 2:
                c.callproc('cartridge_search', (s_value,))
                cr = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()
            print(cr)
            return render(request, 'main/index.html',
                          context={'all_result': ar, 'error_result': er, 'cartridge_result': cr})
