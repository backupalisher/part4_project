from django.shortcuts import render
from django.http import HttpResponse, Http404
import db_model.models as models
from django.db import connections
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
    brands = models.Brands.objects.all()
    return render(request, 'brands/index.html', {'title': title, 'brands': brands})

def index(request, brand_id):
    try:
        page = int(request.GET.get('page'))
    except:
        page = 0
    limit = 50
    offset = 50 * page
    q_model = "SELECT d.id, mo.name model_name, mo.main_image, mo.image FROM models mo LEFT JOIN details d ON mo.id = d.model_id WHERE mo.brand_id = %d and d.module_id is NULL ORDER BY d.id LIMIT %d OFFSET %d" % (brand_id, limit, offset)
    brand_models = _query(q_model)
    model_count = _query(f'SELECT COUNT(id) from (SELECT d.id, mo.name model_name, mo.main_image, mo.image FROM models mo LEFT JOIN details d ON mo.id = d.model_id WHERE mo.brand_id = {brand_id} and d.module_id is NULL ORDER BY d.id) as f')
    brand_name = models.Brands.objects.filter(id=brand_id).values('name')[0]['name']
    pages = math.ceil(int(model_count[0][0]) / limit)
    print(pages)
    return render(request, 'brand/index.html', {'brand_models': brand_models, 'brand_name': brand_name,
                                                'model_count': model_count, 'page': page, 'pages': range(pages)})