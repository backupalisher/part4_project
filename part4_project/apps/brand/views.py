from django.shortcuts import render
from django.http import HttpResponse, Http404
import db_model.models as models
from django.db import connections
from django import forms
import math

def _query(q):
    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.execute(q)
            data = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()
            return data

# Create your views here.
def brands(request):
    title = 'Бренды'
    brands = models.Brands.objects.all().order_by('name')
    return render(request, 'brands/index.html', {'title': title, 'brands': brands})

def index(request, brand_id):
    sfilter = models.FilterSettings.objects.all().order_by('id')
    filter_captions = ['Общие характеристики','Принтер','Копир','Сканер','Расходные материалы','Лотки','Финишер','Интерфейсы']

    print(request.POST)

    try:
        page = int(request.GET.get('page'))
    except:
        page = 0
    limit = 5000
    offset = 50 * page
    #q_model = "SELECT d.id, mo.name model_name, mo.main_image, mo.image FROM models mo LEFT JOIN details d ON mo.id = d.model_id WHERE mo.brand_id = %d and d.module_id is NULL ORDER BY d.id LIMIT %d OFFSET %d" % (brand_id, limit, offset)
    brand_models = _query(f'SELECT d.id, m.*, opt_ids FROM ( SELECT detail_id, array_agg(detail_option_id) opt_ids FROM link_details_options GROUP BY detail_id) ldoi LEFT JOIN details d ON ldoi.detail_id = d.id LEFT JOIN models m ON d.model_id = m.id WHERE brand_id = {brand_id} ORDER BY m.id;')
    model_count = _query(f'SELECT COUNT(id) from (SELECT d.id, mo.name model_name, mo.main_image, mo.image FROM models mo LEFT JOIN details d ON mo.id = d.model_id WHERE mo.brand_id = {brand_id} and d.module_id is NULL ORDER BY d.id) as f')
    brand_name = models.Brands.objects.filter(id=brand_id).values('name')[0]['name']
    pages = math.ceil(int(model_count[0][0]) / limit)
    print(pages)
    return render(request, 'brand/index.html', {'brand_models': brand_models, 'brand_name': brand_name,
                                                'model_count': model_count, 'page': page, 'pages': range(pages),
                                                'sfilter': sfilter, 'filter_captions': filter_captions})