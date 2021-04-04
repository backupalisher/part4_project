import concurrent.futures
import datetime
import asyncio
import json
import math

from django.http import JsonResponse
from django.shortcuts import render

from db_model import models
from functions.main import GetModels as gm, search_init, get_filters, get_all_models, get_partcodes

from db_model import *
from main_views.model_views import model_index

filter_captions = [
    ['Общие характеристики', 'Common options'],
    ['Принтер', 'Printer'],
    ['Копир', 'Copier'],
    ['Сканер', 'Scanner'],
    ['Расходные материалы', 'Consumables'],
    ['Лотки', 'Feeder'],
    ['Финишер', 'Finisher'],
    ['Интерфейсы', 'Interface']
]
start_time = datetime.datetime.now()


def index(request, path):
    lang = request.LANGUAGE_CODE
    brands = models.Brands.objects.filter(logotype__isnull=False)
    base_context = {
        'lang': lang,
        'filter_captions': filter_captions,
        'brands': brands
    }
    if 'model/' in path:
        model_id = int(path.replace('model/', ''))
        template, context = model_index(request, model_id)
        context.update(base_context)
        sfilter = get_filters()
        context.update({'sfilter': sfilter})
        return render(request, template, context)
    if path.replace('/', '') == 'models':
        template, context = index_models(request)
        context.update(base_context)
        sfilter = get_filters()
        context.update({'sfilter': sfilter})
        return render(request, template, context)
    elif path.replace('/', '') == 'market':
        template, context = index_market(request)
        context.update(base_context)
        sfilter = get_filters()
        context.update({'sfilter': sfilter})
        return render(request, template, context)
    elif path.replace('/', '') == 'supplies':
        template, context = index_supplies(request)
        context.update(base_context)
        return render(request, template, context)
    elif path.replace('/', '') == 'about':
        template, context = index_about(request)
        context.update(base_context)
        return render(request, template, context)
    elif path.replace('/', '') == 'search':
        template, context = search(request)
        context.update(base_context)
        return render(request, template, context)
    else:
        template, context = index_models(request)
        context.update(base_context)
        sfilter = get_filters()
        context.update({'sfilter': sfilter})
        return render(request, template, context)


def search(request):
    s_value = ''
    for item in request.GET:
        if 's' in item:
            s_value = request.GET.__getitem__('s')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    result = loop.run_until_complete(search_init(s_value))
    pr = result[0]
    er = result[1]
    cr = result[2]
    mr = result[3]
    pr_set = []
    for x in pr:
        try:
            idx = pr_set.index(x)
        except:
            pr_set.append(x)
    return 'main/search.html', {'all_result': pr_set, 'error_result': er, 'cartridge_result': cr, 'model_result': mr}


def index_about(request):
    title = 'About'
    return 'about/index.html', {'title': title}


def index_supplies(request):
    if request.is_ajax():
        if request.method == 'POST':
            brand_id = ''
            for bid in json.loads(request.POST['brands']):
                if brand_id == '':
                    brand_id += str(bid)
                else:
                    brand_id += ',' + str(bid)
            supplies = get_partcodes(target='supplies', brand_id=brand_id)
            request.session['supplies'] = supplies
            return 'supplies/supplies.html', {'supplies': supplies}
    else:
        supplies = get_partcodes('supplies')
        request.session['supplies'] = supplies
        return 'supplies/index.html', {'supplies': supplies}


def index_market(request):
    try:
        page = int(request.GET.get('page'))
    except:
        page = 0
    limit = 200
    offset = 24 * page
    brand_models = get_all_models(limit, offset, 'market')
    request.session['brand_models'] = brand_models
    if brand_models:
        model_count = len(brand_models)
    else:
        model_count = 0
    pages = math.ceil(model_count / limit)
    return 'market/index.html', {'search_block': True, 'brand_models': brand_models, 'model_count': model_count,
                                 'page': page, 'pages': range(pages)}


def index_models(request):
    pages = 0
    try:
        page = int(request.GET.get('page'))
    except:
        page = 0
    limit = 200
    offset = 24 * page

    if request.is_ajax():
        if request.method == 'POST':
            print(request.POST)
            if dict(request.POST.lists())['reset'][0] and 'true' in dict(request.POST.lists())['reset'][0]:
                brand_models = get_all_models(limit, offset, '')
                model_count = len(brand_models)
                pages = math.ceil(model_count / limit)
            else:
                brand_models = gm().filtered(request.POST)
                if brand_models:
                    model_count = len(brand_models)
                else:
                    brand_models = request.session['brand_models']
                    if brand_models:
                        model_count = len(brand_models)
                    else:
                        brand_models = get_all_models(limit, offset, '')
                        model_count = len(brand_models)
                        pages = math.ceil(model_count / limit)
            return 'filter/filter_result.html', {'search_block': True, 'page': page,
                                                 'pages': range(pages), 'brand_models': str(brand_models),
                                                 'model_count': model_count}
        else:
            return JsonResponse('unsuccessful')
    else:
        brand_models = get_all_models(limit, offset, '')
        return 'main/models.html', {'search_block': True, 'brand_models': brand_models}
