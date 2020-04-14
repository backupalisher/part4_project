import math
from django.shortcuts import render
from django.http import HttpResponse, Http404
import db_model.models as models
from django.db import connections
from django import forms

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
    for i, rid in enumerate(rids):
        if i == 0:
            sq = (f' mopt.ids @> ARRAY[{rid[0]}]')
        else:
            sq += (f' OR mopt.ids @> ARRAY[{rid[0]}]')
    return sq

def sql_gen_checks(checks):
    cq = ' mopt.ids @> ARRAY['
    for i, check in enumerate(checks):
        if i == 0:
            cq += (f'{check}')
        else:
            cq += (f',{check}')
    cq += ']'
    print(cq)
    return cq

def index(request, brand_id):
    sfilter = models.FilterSettings.objects.all().order_by('id')
    filter_captions = ['Общие характеристики', 'Принтер', 'Копир', 'Сканер', 'Расходные материалы', 'Лотки', 'Финишер',
                       'Интерфейсы']

    # Base sql part of query for get model by filter
    f_sql = (
        f'SELECT * FROM (SELECT d.id did, m.id mid, m.name model, array_agg(ldo.detail_option_id) ids FROM models m LEFT JOIN details d ON d.model_id = m.id LEFT JOIN link_details_options ldo ON ldo.detail_id = d.id WHERE d.module_id is null and m.brand_id = {brand_id} GROUP BY did, mid, model ORDER BY mid) mopt WHERE ')
    filterDict = dict(request.POST.lists())
    ops = 0
    for req in filterDict:
        if 'range' in req:
            if filterDict[req][0] != '' or filterDict[req][1] != '':
                if ops == 0:
                    f_sql += sql_get_range(req.replace('range', ''), filterDict[req][0], filterDict[req][1])
                    ops += 1
                else:
                    f_sql += ' OR '
                    f_sql += sql_get_range(req.replace('range', ''), filterDict[req][0], filterDict[req][1])
        elif 'radio' in req:
            if ops == 0:
                f_sql += (f'mopt.ids @> ARRAY[{filterDict[req][0]}]')
                ops += 1
            else:
                f_sql += ' OR '
                f_sql += (f'mopt.ids @> ARRAY[{filterDict[req][0]}]')
        elif 'checkbox' in req:
            if ops == 0:
                f_sql += sql_gen_checks(filterDict[req])
                ops += 1
            else:
                f_sql += ' OR '
                f_sql += sql_gen_checks(filterDict[req])
    try:
        page = int(request.GET.get('page'))
    except:
        page = 0
    limit = 24
    offset = 24 * page
    # q_model = "SELECT d.id, mo.name model_name, mo.main_image, mo.image FROM models mo LEFT JOIN details d ON mo.id = d.model_id WHERE mo.brand_id = %d and d.module_id is NULL ORDER BY d.id LIMIT %d OFFSET %d" % (brand_id, limit, offset)
    if ops > 0:
        brand_models = _query(f_sql)
    else:
        brand_models = _query(f'SELECT d.id, m.* FROM models m LEFT JOIN details d ON m.id = d.model_id AND d.partcode_id is NULL WHERE brand_id = {brand_id} ORDER BY m.id LIMIT {limit} OFFSET {offset};')
            # _query(
            # f'SELECT d.id, m.*, opt_ids FROM ( SELECT detail_id, array_agg(detail_option_id) opt_ids '
            # f'FROM link_details_options GROUP BY detail_id) ldoi LEFT JOIN details d ON ldoi.detail_id = d.id '
            # f'LEFT JOIN models m ON d.model_id = m.id WHERE brand_id = {brand_id} ORDER BY m.id;')
    model_count = _query(
        f'SELECT COUNT(id) from (SELECT d.id, mo.name model_name, mo.main_image, mo.image '
        f'FROM models mo LEFT JOIN details d ON mo.id = d.model_id WHERE mo.brand_id = {brand_id} and d.module_id is NULL ORDER BY d.id) as f')
    brand_name = models.Brands.objects.filter(id=brand_id).values('name')[0]['name']
    pages = math.ceil(int(model_count[0][0]) / limit)
    return render(request, 'brand/index.html', {'brand_models': brand_models, 'brand_name': brand_name,
                                                'model_count': model_count, 'page': page, 'pages': range(pages),
                                                'sfilter': sfilter, 'filter_captions': filter_captions})
