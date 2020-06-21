import asyncio
import concurrent.futures
import datetime

from asgiref.sync import sync_to_async
from django.http import Http404
from django.shortcuts import render

import db_model.models as models
from db_model.db_utils import _query

start_time = datetime.datetime.now()


def detail_view(request):
    return render(request, 'detail/index.html')


# добавление веса
@sync_to_async
def set_weight(detail_id):
    print(datetime.datetime.now() - start_time, 'обновление веса')
    _query(
        f"UPDATE details SET weight = (w.weight+1) FROM (SELECT weight FROM details WHERE id = {detail_id}) w "
        f"WHERE id = {detail_id}")
    print(datetime.datetime.now() - start_time, 'обновление веса завершено')


@sync_to_async
def get_ids(detail_id):
    pass


@sync_to_async
def get_options(detail_id):
    print(datetime.datetime.now() - start_time, 'Запрос на получение опций')
    q_options = f"SELECT * FROM all_options_for_details WHERE detail_id = {detail_id}"
    option_vals = _query(q_options)
    print(datetime.datetime.now() - start_time, 'Запрос на получение опций завершен')
    print(datetime.datetime.now() - start_time, 'Сортировка опций')
    captions = []
    subcaptions = []
    values = []
    for opts in option_vals:
        if opts[0] is None and opts[1] is None:
            for i in range(len(opts[3])):
                opts[3][i] = opts[3][i].replace('Caption: ', '')
            captions.append(opts)
        if opts[0] is None and opts[1] is not None:
            for opt in opts[3]:
                if 'SubCaption' in opt:
                    opts[3].remove(opt)
            subcaptions.append(opts)
        else:
            values.append(opts)
    options = option_vals
    print(datetime.datetime.now() - start_time, 'Сортировка опций завершена')
    return options, captions, subcaptions, values


@sync_to_async
def get_cartridge_options(partcode):
    print(datetime.datetime.now() - start_time, 'Запрос на получение картриджей')
    cartridge_options = _query(f"SELECT * FROM all_options_for_cartridges WHERE code = '{partcode}'")
    print(datetime.datetime.now() - start_time, 'Запрос на получение картриджей завершен')
    return cartridge_options


@sync_to_async
def get_partcodes(model_id):
    print(datetime.datetime.now() - start_time, 'Запрос на получение парткаталога')
    partcatalog = _query(f"SELECT * FROM all_partcatalog WHERE model_id = {model_id}")
    print(datetime.datetime.now() - start_time, 'Запрос на получение парткаталога завершен')
    return partcatalog


async def init(detail_id):
    async_tasks = [get_options(detail_id), get_ids(detail_id)]
    results = await asyncio.gather(*async_tasks)
    return results


async def past_init(request, model_id, partcode):
    if partcode != '-':
        tasks = [
            # get_partcodes(model_id),
            get_cartridge_options(partcode),
        ]
        results = await asyncio.gather(*tasks)
        return results
    else:
        return []


def index(request, detail_id):
    print(start_time, detail_id)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    loop.create_task(set_weight(detail_id))
    print(datetime.datetime.now() - start_time, 'start')
    init_result = loop.run_until_complete(init(detail_id))
    options = init_result[0][0]
    captions = init_result[0][1]
    subcaptions = init_result[0][2]
    values = init_result[0][3]
    try:
        try:
            partcode_id = models.Details.objects.filter(id=detail_id).values('partcode_id')[0]['partcode_id']
            partcode = models.Partcodes.objects.filter(id=partcode_id).values().values('code')[0]['code']
            partcodes = list(models.Partcodes.objects.filter(id=partcode_id).values())[0]
        except:
            partcodes = []
            partcode = '-'
        try:
            model_id = models.Details.objects.filter(id=detail_id).values('model_id')[0]['model_id']
            model = models.Models.objects.filter(id=model_id).values('name')[0]['name']
        except:
            model_id = None
            model = '-'
        try:
            module_id = models.Details.objects.filter(id=detail_id).values('module_id')[0]['module_id']
            module = list(models.SprModules.objects.filter(id=module_id).values())[0]
        except:
            module = '-'
        try:
            spr_detail_id = models.Details.objects.filter(id=detail_id).values('spr_detail_id')[0]['spr_detail_id']
            if models.SprDetails.objects.filter(id=spr_detail_id).values('name_ru')[0]['name_ru'] != None:
                detail_name = models.SprDetails.objects.filter(id=spr_detail_id).values('name_ru')[0]['name_ru']
            else:
                detail_name = models.SprDetails.objects.filter(id=spr_detail_id).values('name')[0]['name']
        except:
            detail_name = '-'
        post_result = loop.run_until_complete(past_init(request, model_id, partcode))
        # partcatalog = post_result[0]
        cartridge_options = post_result[0]
        brand_id = models.Models.objects.filter(id=model_id).values('brand_id')[0]['brand_id']
        brand_name = models.Brands.objects.filter(id=brand_id).values('name')[0]['name']

    except:
        raise Http404('Страница отсутствует, с id: ' + str(detail_id))

    return render(request, 'detail/index.html',
                  {'partcodes': partcodes, 'detail_id': detail_id, 'model': model, 'model_id': model_id,
                   'module': module, 'detail_name': detail_name, 'options': options,
                   'captions': captions, 'subcaptions': subcaptions, 'values': values,
                   'brand_id': brand_id, 'brand_name': brand_name, 'cartridge_options': cartridge_options})
