import math

from django.db import connections
from django.shortcuts import render

import db_model.models as models


def _query(q):
    data = None
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


# Function for get option ids from range and generate sql parts
def sql_get_range(cid, rmin, rmax):
    if rmin:
        pass
    else:
        rmin = 0
    if rmax:
        pass
    else:
        rmax = 1000000
    q = (f'SELECT * FROM select_id_for_range({cid}, {rmin}, {rmax})')
    rids = _query(q)
    sq = ''
    for i, rid in enumerate(rids):
        if i == 0:
            sq = (f' mopt.ids && ARRAY[{rid[0]}]')
        else:
            sq += (f' OR mopt.ids && ARRAY[{rid[0]}]')
    return sq


def sql_gen_checks(checks):
    cq = ' mopt.ids && ARRAY['
    for i, check in enumerate(checks):
        if i == 0:
            cq += (f'{check}')
        else:
            cq += (f',{check}')
    cq += ']'
    print(cq)
    return cq


def index(request, brand_id):
    model_count = 0
    sfilter = models.FilterSettings.objects.all().order_by('id')
    filter_captions = ['Общие характеристики', 'Принтер', 'Копир', 'Сканер', 'Расходные материалы', 'Лотки', 'Финишер',
                       'Интерфейсы']

    # Base sql part of query for get model by filter
    f_sql = (
        f'SELECT * FROM (SELECT d.id did, m.id mid, m.name model, array_agg(ldo.detail_option_id) ids,'
        f' m.main_image, m.image FROM models m LEFT JOIN details d ON d.model_id = m.id '
        f'LEFT JOIN link_details_options ldo ON ldo.detail_id = d.id '
        f'WHERE d.module_id is null and m.brand_id = {brand_id} GROUP BY did, mid, model, m.main_image, m.image '
        f'ORDER BY mid) mopt WHERE ')
    filterDict = dict(request.POST.lists())
    ops = 0
    for req in filterDict:
        if 'range' in req:
            if filterDict[req][0] != '' or filterDict[req][1] != '':
                if ops == 0:
                    f_sql += sql_get_range(req.replace('range', ''), filterDict[req][0], filterDict[req][1])
                    ops += 1
                else:
                    f_sql += ' AND '
                    f_sql += sql_get_range(req.replace('range', ''), filterDict[req][0], filterDict[req][1])
        elif 'radio' in req:
            if ops == 0:
                f_sql += (f'mopt.ids && ARRAY[{filterDict[req][0]}]')
                ops += 1
            else:
                f_sql += ' AND '
                f_sql += (f'mopt.ids && ARRAY[{filterDict[req][0]}]')
        elif 'checkbox' in req:
            if ops == 0:
                f_sql += sql_gen_checks(filterDict[req])
                ops += 1
            else:
                f_sql += ' AND '
                f_sql += sql_gen_checks(filterDict[req])
    try:
        page = int(request.GET.get('page'))
    except:
        page = 0
    limit = 2400
    offset = 2400 * page
    if ops > 0:
        print(f_sql)
        brand_models = _query(f_sql)
        if brand_models:
            model_count = len(brand_models)
        pages = 0
    else:
        brand_models = _query(f'SELECT d.id, m.* FROM models m '
                              f'LEFT JOIN details d ON m.id = d.model_id AND d.partcode_id is NULL '
                              f'WHERE brand_id = {brand_id} ORDER BY m.id LIMIT {limit} OFFSET {offset};')
        model_count = _query(f'SELECT COUNT(id) from (SELECT d.id, mo.name model_name, mo.main_image, mo.image '
                             f'FROM models mo LEFT JOIN details d ON mo.id = d.model_id '
                             f'WHERE mo.brand_id = {brand_id} and d.module_id is NULL ORDER BY d.id) as f')
        pages = math.ceil(int(model_count[0][0]) / limit)

    brand_name = models.Brands.objects.filter(id=brand_id).values('name')[0]['name']
    return render(request, 'brand/index.html', {'brand_models': brand_models, 'brand_name': brand_name,
                                                'model_count': model_count, 'page': page, 'pages': range(pages),
                                                'sfilter': sfilter, 'filter_captions': filter_captions})
