import math

from asgiref.sync import sync_to_async
from django.db import connections
from django.shortcuts import render
import db_model.models as models
import datetime
import asyncio
start_time = datetime.datetime.now()

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
    return cq


@sync_to_async
def get_filters():
    print(datetime.datetime.now() - start_time, 'получение фильтров')
    sfilter = models.FilterSettings.objects.all().order_by('id')
    print(datetime.datetime.now() - start_time, 'получение фильтров завершено')
    return sfilter


@sync_to_async
def get_all_models(brand_id, limit, offset):
    print(datetime.datetime.now() - start_time, 'получение всех моделей')
    brand_models = _query(f'SELECT d.id, m.*, b.name FROM (SELECT name FROM brands WHERE id={brand_id}) b, models m '
                          f'LEFT JOIN details d ON m.id = d.model_id AND d.partcode_id is NULL '
                          f'WHERE brand_id = {brand_id} ORDER BY m.id LIMIT {limit} OFFSET {offset};')
    print(datetime.datetime.now() - start_time, 'получение всех моделей завершено')
    return brand_models


@sync_to_async
def get_filtered_model(brand_id, post_filter):
    f_sql = (
        f'SELECT * FROM (SELECT * FROM '
        f'(SELECT d.id did, m.id mid, m.name model, array_agg(ldo.detail_option_id) ids,'
        f' m.main_image, m.image FROM models m LEFT JOIN details d ON d.model_id = m.id '
        f'LEFT JOIN link_details_options ldo ON ldo.detail_id = d.id '
        f'WHERE d.module_id is null and m.brand_id = {brand_id} GROUP BY did, mid, model, m.main_image, m.image '
        f'ORDER BY mid) mopt WHERE ')
    filterDict = dict(post_filter)
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
    f_sql = f_sql+') d , (SELECT name FROM brands WHERE id=1) b'
    brand_models = _query(f_sql)
    return brand_models


async def preload(brand_id, limit, offset):
    tasks = [get_filters(), get_all_models(brand_id, limit, offset)]
    results = await asyncio.gather(*tasks)
    return results


async def fpreload(brand_id, post_filter):
    tasks = [get_filters(), get_filtered_model(brand_id, post_filter)]
    results = await asyncio.gather(*tasks)
    return results


def index(request, brand_id):
    print(start_time, brand_id)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    model_count = 0
    pages = 0
    try:
        page = int(request.GET.get('page'))
    except:
        page = 0
    limit = 2400
    offset = 2400 * page
    brand_models = []
    filter_captions = ['Общие характеристики', 'Принтер', 'Копир', 'Сканер', 'Расходные материалы', 'Лотки', 'Финишер',
                       'Интерфейсы']
    post_filter = dict(request.POST.lists())
    if len(post_filter) != 0:
        print('filter apply')
        fload = loop.run_until_complete(fpreload(brand_id, post_filter))
        sfilter = fload[0]
        # Base sql part of query for get model by filter
        brand_models = fload[1]
        brand_name = fload[1][0][6]
        if brand_models:
            model_count = len(brand_models)
    else:
        preloads = loop.run_until_complete(preload(brand_id, limit, offset))
        sfilter = preloads[0]
        brand_models = preloads[1]
        brand_name = preloads[1][0][6]
        model_count = len(brand_models)
        print(model_count)
        pages = math.ceil(model_count / limit)
    loop.close()
    print(datetime.datetime.now() - start_time, 'завершение')
    return render(request, 'brand/index.html', {'brand_models': brand_models, 'brand_name': brand_name,
                                                'model_count': model_count, 'page': page, 'pages': range(pages),
                                                'sfilter': sfilter, 'filter_captions': filter_captions})
