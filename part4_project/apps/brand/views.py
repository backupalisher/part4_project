import asyncio
import datetime
import json
import math

from asgiref.sync import sync_to_async
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
import concurrent.futures

import db_model.models as models
from db_model.db_utils import _query

start_time = datetime.datetime.now()


# Create your views here.
def brands(request):
    title = 'Бренды'
    brands = models.Brands.objects.all()
    if request.is_ajax():
        if request.method == 'POST':
            formdata = request.POST
            formValues = formdata.getlist('formValues')
            q = QueryDict(formValues[0]).lists()
            brand_name = ''
            for data in q:
                if data[0] == 'brand_name':
                    brand_name = data[1][0]
            if brand_name != '':
                brands = list(models.Brands.objects.filter(name=brand_name).values())
            title = 'Бренды'
            return render(request, 'brands/ajax.html', {'title': title, 'brands': brands})
            # return JsonResponse({'results': brands})
        else:
            return JsonResponse('unsuccessful')
    else:
        return render(request, 'brands/index.html', {'title': title, 'brands': brands})


def ajax(request):
    if request.method == 'POST':
        formdata = request.POST
        formValues = formdata.getlist('formValues')
        q = QueryDict(formValues[0]).lists()
        brand_name = ''
        for data in q:
            if data[0] == 'brand_name':
                brand_name = data[1][0]
        brands = list(models.Brands.objects.filter(name=brand_name).values())
        title = 'Бренды'
        return render(request, 'brands/index.html', {'title': title, 'brands': brands})
        # return JsonResponse({'results': brands})
    else:
        return JsonResponse('unsuccessful')


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
    q = f'SELECT * FROM select_id_for_range({cid}, {rmin}, {rmax})'
    rids = _query(q)
    sq = ''
    for i, rid in enumerate(rids):
        if i == 0:
            sq = f' mopt.ids && ARRAY[{rid[0]}]'
        else:
            sq += f' OR mopt.ids && ARRAY[{rid[0]}]'
    return sq


def sql_gen_checks(checks):
    cq = ' mopt.ids && ARRAY['
    for i, check in enumerate(checks):
        if i == 0:
            cq += f'{check}'
        else:
            cq += f',{check}'
    cq += '] '
    return cq


@sync_to_async
def get_filters():
    # print(datetime.datetime.now() - start_time, 'получение фильтров')
    sfilter = models.FilterSettings.objects.all().order_by('id')
    # print(datetime.datetime.now() - start_time, 'получение фильтров завершено')
    return sfilter


@sync_to_async
def get_all_models(brand_id, limit, offset):
    # print(datetime.datetime.now() - start_time, 'получение всех моделей')
    brand_models = _query(
        f'SELECT * FROM model_for_filter mopt WHERE brand_id = {brand_id} ORDER BY main_image LIMIT {limit} OFFSET {offset};')
    # print(datetime.datetime.now() - start_time, 'получение всех моделей завершено')
    return brand_models


@sync_to_async
def get_filtered_model(brand_id, checkboxs, ranges, radios):
    checkboxs = json.loads(str(checkboxs))
    ranges = json.loads(str(ranges))
    radios = json.loads(str(radios))
    f_sql = f'SELECT * FROM model_for_filter mopt WHERE ('
    ops = 0
    for key, value in ranges.items():
        if len(value) > 0:
            if ops == 0:
                f_sql += sql_get_range(key.replace('range', ''), value[0], value[1])
                ops += 1
            else:
                f_sql += ' AND '
                f_sql += sql_get_range(key.replace('range', ''), value[0], value[1])
    for key, value in radios.items():
        if len(value) > 0:
            if ops == 0:
                f_sql += (f'mopt.ids && ARRAY[{value}]')
                ops += 1
            else:
                f_sql += ' AND '
                f_sql += (f'mopt.ids && ARRAY[{value}]')
    for key, value in checkboxs.items():
        if len(value) > 0:
            if ops == 0:
                f_sql += sql_gen_checks(value)
                ops += 1
            else:
                f_sql += ' AND '
                f_sql += sql_gen_checks(value)
    f_sql += f' ) AND brand_id = {brand_id} ORDER BY main_image;'
    print(f_sql)
    brand_models = _query(f_sql)
    return brand_models


async def preload(brand_id, limit, offset):
    tasks = [get_filters(), get_all_models(brand_id, limit, offset)]
    results = await asyncio.gather(*tasks)
    return results


async def fpreload(brand_id, checkboxs, ranges, radios):
    tasks = [get_filtered_model(brand_id, checkboxs, ranges, radios)]
    results = await asyncio.gather(*tasks)
    return results


def index(request, brand_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    model_count = 0
    pages = 0
    try:
        page = int(request.GET.get('page'))
    except:
        page = 0
    limit = 24000
    offset = 24 * page
    brand_models = []
    checkboxs = {}
    ranges = {}
    radios = {}
    if request.is_ajax():
        if request.method == 'POST':
            brand_models = request.session['brand_models']

            model_count = len(brand_models)
            if dict(request.POST.lists())['checkboxs'][0]:
                checkboxs = dict(request.POST.lists())['checkboxs'][0]
            if dict(request.POST.lists())['ranges'][0]:
                ranges = dict(request.POST.lists())['ranges'][0]
            if dict(request.POST.lists())['radios'][0]:
                radios = dict(request.POST.lists())['radios'][0]
            if len(checkboxs) != 0 or len(ranges) != 0 or len(radios) != 0:
                print('filter')
                fload = loop.run_until_complete(fpreload(brand_id, checkboxs, ranges, radios))
                # Base sql part of query for get model by filter
                brand_models = fload[0]
                if brand_models:
                    model_count = len(brand_models)
            else:
                preloads = loop.run_until_complete(preload(brand_id, limit, offset))
                sfilter = preloads[0]
                brand_models = preloads[1]
                model_count = len(brand_models)
                pages = math.ceil(model_count / limit)
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
            return render(request, 'filter/filter_result.html', {'page': page, 'pages': range(pages),
                                                                 'brand_models': str(brand_models),
                                                                 'model_count': model_count})
        else:
            return JsonResponse('unsuccessful')
    else:
        # print(start_time, brand_id)
        filter_captions = ['Общие характеристики', 'Принтер', 'Копир', 'Сканер', 'Расходные материалы', 'Лотки',
                           'Финишер',
                           'Интерфейсы']
        brand_name = models.Brands.objects.filter(id=brand_id).values('name')[0]['name']
        preloads = loop.run_until_complete(preload(brand_id, limit, offset))
        sfilter = preloads[0]
        brand_models = preloads[1]
        request.session['brand_models'] = brand_models
        model_count = len(brand_models)
        pages = math.ceil(model_count / limit)
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        # print(datetime.datetime.now() - start_time, 'завершение')
        return render(request, 'brand/index.html', {'brand_models': brand_models, 'brand_name': brand_name,
                                                    'model_count': model_count, 'page': page, 'pages': range(pages),
                                                    'sfilter': sfilter, 'filter_captions': filter_captions})
