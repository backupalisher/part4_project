import concurrent.futures
import datetime

from django.http import JsonResponse
from django.shortcuts import render

import db_model.models as models
from .functions import *

start_time = datetime.datetime.now()


def index(request):
    brands = models.Brands.objects.all()
    return render(request, 'main/index.html', context={'search_block': True, 'brands': brands})


def search(request):
    variant = 0
    s_value = ''
    for item in request.GET:
        if 's' in item:
            s_value = request.GET.__getitem__('s')
        if 'v' in item:
            variant = int(request.GET.__getitem__('v'))
    ar = None
    er = None
    cr = None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    result = loop.run_until_complete(search_init(s_value))
    ar = result[0]
    er = result[1]
    cr = result[2]
    return render(request, 'main/search.html',
                  context={'all_result': ar, 'error_result': er, 'cartridge_result': cr})


def index_models(request):
    lang = request.LANGUAGE_CODE
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    model_count = 0
    pages = 0
    filter_captions = ['Общие характеристики', 'Принтер', 'Копир', 'Сканер', 'Расходные материалы', 'Лотки',
                       'Финишер',
                       'Интерфейсы']
    try:
        page = int(request.GET.get('page'))
    except:
        page = 0
    limit = 200
    offset = 24 * page
    brand_models = []
    checkboxs = {}
    ranges = {}
    radios = {}
    brands = models.Brands.objects.all()
    fbrands = []
    if request.is_ajax():
        if request.method == 'POST':
            if dict(request.POST.lists())['reset'][0] and 'true' in dict(request.POST.lists())['reset'][0]:
                preloads = loop.run_until_complete(preload(limit, offset))
                brand_models = preloads[1]
                model_count = len(brand_models)
                pages = math.ceil(model_count / limit)
                loop.run_until_complete(loop.shutdown_asyncgens())
                loop.close()
            else:
                brand_models = request.session['brand_models']
                model_count = len(brand_models)
                if dict(request.POST.lists())['checkboxs'][0]:
                    checkboxs = dict(request.POST.lists())['checkboxs'][0]
                if dict(request.POST.lists())['ranges'][0]:
                    ranges = dict(request.POST.lists())['ranges'][0]
                if dict(request.POST.lists())['radios'][0]:
                    radios = dict(request.POST.lists())['radios'][0]
                if dict(request.POST.lists())['brands'][0] and 'null' not in dict(request.POST.lists())['brands'][0]:
                    fbrands = dict(request.POST.lists())['brands'][0].replace('[', '').replace(']', '').split(',')
                if len(checkboxs) != 0 or len(ranges) != 0 or len(radios) != 0:
                    fload = loop.run_until_complete(fpreload(fbrands, checkboxs, ranges, radios))
                    # Base sql part of query for get model by filter
                    brand_models = fload[0]
                    if brand_models:
                        model_count = len(brand_models)
                else:
                    preloads = loop.run_until_complete(preload(limit, offset))
                    sfilter = preloads[0]
                    brand_models = preloads[1]
                    model_count = len(brand_models)
                    pages = math.ceil(model_count / limit)
                loop.run_until_complete(loop.shutdown_asyncgens())
                loop.close()
            return render(request, 'filter/filter_result.html', {'search_block': True, 'brands': brands,
                                                                 'page': page, 'pages': range(pages),
                                                                 'brand_models': str(brand_models),
                                                                 'model_count': model_count, 'lang': lang})
        else:
            return JsonResponse('unsuccessful')
    else:
        # print(start_time, brand_id)
        preloads = loop.run_until_complete(preload(limit, offset))
        sfilter = preloads[0]
        brand_models = preloads[1]
        request.session['brand_models'] = brand_models
        model_count = len(brand_models)
        pages = math.ceil(model_count / limit)
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        # print(datetime.datetime.now() - start_time, 'завершение')
        return render(request, 'main/models.html', {'search_block': True, 'brands': brands,
                                                    'brand_models': brand_models, 'lang': lang,
                                                    'model_count': model_count, 'page': page, 'pages': range(pages),
                                                    'sfilter': sfilter, 'filter_captions': filter_captions})
