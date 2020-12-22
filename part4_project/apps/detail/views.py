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
    print('set weight', detail_id)
    # print(datetime.datetime.now() - start_time, 'обновление веса')
    _query(
        f"UPDATE details SET weight = (w.weight+1) FROM (SELECT weight FROM details WHERE id = {detail_id}) w "
        f"WHERE id = {detail_id}")
    # print(datetime.datetime.now() - start_time, 'обновление веса завершено')


@sync_to_async
def get_detail(detail_id):
    return _query(f"SELECT * FROM all_details WHERE id = {detail_id}")


@sync_to_async
def get_options(detail_id):
    # print(datetime.datetime.now() - start_time, 'Запрос на получение опций')
    q_options = f"SELECT * FROM all_options_for_details WHERE detail_id = {detail_id}"
    option_vals = _query(q_options)
    # print(datetime.datetime.now() - start_time, 'Запрос на получение опций завершен')
    # print(datetime.datetime.now() - start_time, 'Сортировка опций')
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
    # print(datetime.datetime.now() - start_time, 'Сортировка опций завершена')
    return options, captions, subcaptions, values


@sync_to_async
def get_cartridge_options(partcode):
    # print(datetime.datetime.now() - start_time, 'Запрос на получение картриджей')
    cartridge_options = _query(f"SELECT * FROM all_options_for_cartridges WHERE code = '{partcode}'")
    # print(datetime.datetime.now() - start_time, 'Запрос на получение картриджей завершен')
    return cartridge_options


async def init(detail_id):
    async_tasks = [get_options(detail_id), get_detail(detail_id)]
    results = await asyncio.gather(*async_tasks)
    return results


async def past_init(request, partcode):
    if partcode != '-':
        tasks = [
            get_cartridge_options(partcode),
        ]
        results = await asyncio.gather(*tasks)
        return results
    else:
        return []


def index(request, detail_id):
    lang = request.LANGUAGE_CODE
    # print(start_time, detail_id)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    loop.create_task(set_weight(detail_id))
    # print(datetime.datetime.now() - start_time, 'start')
    init_result = loop.run_until_complete(init(detail_id))
    try:
        try:
            options = init_result[0][0]
            captions = init_result[0][1]
            subcaptions = init_result[0][2]
            values = init_result[0][3]
        except:
            options = None
            captions = None
            subcaptions = None
            values = None
        detail_name = init_result[1][0][1]
        detail_name_ru = init_result[1][0][2]
        model_id = init_result[1][0][3]
        model_name = init_result[1][0][4]
        module_id = init_result[1][0][5]
        module_name = init_result[1][0][6]
        module_name_ru = init_result[1][0][7]
        partcode = init_result[1][0][8]
        part_desc = init_result[1][0][9]
        images = init_result[1][0][10]
        brand_id = init_result[1][0][11]
        brand_name = init_result[1][0][12]
        price = init_result[1][0][13]
        vendor = init_result[1][0][14]
        try:
            cartridge_options = loop.run_until_complete(get_cartridge_options(partcode))
        except:
            cartridge_options = None
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    except:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        raise Http404('Страница отсутствует, с id: ' + str(detail_id))
    return render(request, 'detail/index.html',
                  {'detail_id': detail_id, 'model_name': model_name, 'model_id': model_id, 'module_id': module_id,
                   'module_name': module_name, 'module_name_ru': module_name_ru, 'detail_name': detail_name,
                   'detail_name_ru': detail_name_ru, 'images': images, 'partcode': partcode,
                   'detail_desc': part_desc, 'options': options, 'captions': captions, 'subcaptions': subcaptions,
                   'values': values, 'brand_id': brand_id, 'brand_name': brand_name, 'lang': lang,
                   'cartridge_options': cartridge_options, 'price': price, 'vendor': vendor})
