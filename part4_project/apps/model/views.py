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
    return render(request, 'model/index.html')


# добавление веса
@sync_to_async
def set_weight(detail_id):
    # print(datetime.datetime.now() - start_time, 'обновление веса')
    _query(
        f"UPDATE details SET weight = (w.weight+1) FROM (SELECT weight FROM details WHERE id = {detail_id}) w "
        f"WHERE id = {detail_id}")
    # print(datetime.datetime.now() - start_time, 'обновление веса завершено')


# Запрос на получение опций и вывод опций
@sync_to_async
def get_options(detail_id):
    captions = [
        'Общие характеристики',
        'Принтер',
        'Копир',
        'Сканер',
        'Расходные материалы',
        'Факс',
        'Телефон',
        'Шрифты и языки управления',
        'Лотки',
        'Финишер',
        'Интерфейсы',
        'Память/Процессор',
        'Дополнительная информация',
        'Фото',
        'Общая информация',
        'Габариты',
        'Снят с производства',
        'Актуальный',
    ]
    subcaptions = []
    values = []
    # print(datetime.datetime.now() - start_time, 'получение опций')
    option_vals = _query(f"SELECT * FROM all_options_model WHERE detail_id = {detail_id};")
    # print(datetime.datetime.now() - start_time, 'получение опций завершено')

    # print(datetime.datetime.now() - start_time, 'сортировка опций')
    for opts in option_vals:
        if opts[0] is None and opts[1] is not None:
            for opt in opts[3]:
                if 'SubCaption' in opt:
                    opts[3].remove(opt)
            subcaptions.append(opts)
        else:
            values.append(opts)
    options = option_vals
    # print(datetime.datetime.now() - start_time, 'сортировка опций завершена')
    return options, captions, subcaptions, values


# Запрос на получение ошибок
@sync_to_async
def get_errors(model_id):
    # print(datetime.datetime.now() - start_time, 'получение ошибок')
    verrors = _query(f"SELECT * FROM all_errors WHERE mid = {model_id}")
    # print(datetime.datetime.now() - start_time, 'получение ошибок завершено')

    # print(datetime.datetime.now() - start_time, 'сортировка ошибок')
    if len(verrors) > 0:
        if verrors[0][2] is None and verrors[0][3] is None and verrors[0][4] is None and verrors[0][5] is None:
            verrors = None
    # print(datetime.datetime.now() - start_time, 'сортировка ошибок завершена')
    return verrors


# Запрос на получение парткодов и модулей
@sync_to_async
def qet_partcatalog(request, model_id):
    # 'Получение id парткодов, моделей, модулей, названий детали для модулей и парткаталога', q_code_module)
    modules = []
    # print(datetime.datetime.now() - start_time, 'получение парткодов и модулей')
    partcatalog = _query(f'SELECT * FROM all_partcatalog WHERE model_id = {model_id}')
    # print(datetime.datetime.now() - start_time, 'получение парткодов и модулей завершено')

    # print(datetime.datetime.now() - start_time, 'Сортировка парткаталога')
    if partcatalog and len(partcatalog) > 0:
        for parts in partcatalog:
            # print(parts)
            if parts[4]:
                modules.append(parts[4])
            elif parts[3]:
                modules.append(parts[3])
        modules = list(dict.fromkeys(modules))
    if request.GET.get('module'):
        cur_module = request.GET.get('module')
    else:
        cur_module = None
    # print(datetime.datetime.now() - start_time, 'Сортировка парткаталога завершена')

    return modules, cur_module, partcatalog


# Запрос на получение id
@sync_to_async
def get_ids(model_id):
    # print(datetime.datetime.now() - start_time, 'сбор id')
    qd = _query(f'SELECT * FROM details WHERE model_id = {model_id} and partcode_id is null')
    try:
        detail_id = qd[0][0]
        spr_detail_id = qd[0][4]
    except:
        detail_id = None
        spr_detail_id = None
    # print(datetime.datetime.now() - start_time, 'сбор id завершен')
    return detail_id, spr_detail_id


@sync_to_async
def get_from_spr_details(spr_detail_id):
    dq = _query(f'SELECT name, name_ru FROM spr_details WHERE id = {spr_detail_id}')
    try:
        if dq[0][1]:
            detail_name = dq[0][1]
        else:
            detail_name = dq[0][0]
    except:
        detail_name = None
    return detail_name


# Получение id парткодов, моделей, бренда, картинок
@sync_to_async
def get_from_models(model_id):
    # print(datetime.datetime.now() - start_time, 'сбор остального')
    mq = _query(f'SELECT brand_id, name, main_image, image FROM models WHERE id = {model_id}')
    try:
        brand_id = mq[0][0]
    except:
        brand_id = None
    try:
        model = mq[0][1]
    except:
        model = None
    try:
        model_main_image = mq[0][2]
    except:
        model_main_image = None
    try:
        model_images = mq[0][3].split(';')
    except:
        model_images = None
    try:
        brand_name = models.Brands.objects.filter(id=brand_id).values('name')[0]['name']
    except:
        brand_name = None
    # print(datetime.datetime.now() - start_time, 'сбор остального завершен')
    return model, model_main_image, model_images, brand_id, brand_name


@sync_to_async
def get_cartridge(model_id):
    # print(datetime.datetime.now() - start_time, 'получение картриджей')
    cartridges = _query(f"SELECT * FROM all_cartridge WHERE {model_id} = ANY(model_id)")
    for idx in range(len(cartridges)):
        cartridge = list(cartridges[idx])
        cartridge[4] = list(set(cartridge[4]))
        cartridges[idx] = tuple(cartridge)
        cartridge_alt = list(cartridges[idx])
        cartridge_alt[8] = list(set(cartridge[8]))
        cartridges[idx] = tuple(cartridge_alt)
    # print(datetime.datetime.now() - start_time, 'получение картриджей завершено')
    return cartridges


async def init(model_id):
    async_tasks = [get_ids(model_id)]
    results = await asyncio.gather(*async_tasks)
    return results


async def past_init(request, model_id, spr_detail_id, detail_id):
    if detail_id:
        tasks = [
            get_from_models(model_id),
            qet_partcatalog(request, model_id),
            get_errors(model_id),
            get_cartridge(model_id),
            get_options(detail_id),
            get_from_spr_details(spr_detail_id)
        ]
    else:
        tasks = [
            get_from_models(model_id),
            qet_partcatalog(request, model_id),
            get_errors(model_id),
            get_cartridge(model_id)
        ]
    results = await asyncio.gather(*tasks)
    return results


def index(request, model_id):
    # print(start_time, model_id)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    # print(datetime.datetime.now() - start_time, 'start')
    init_result = loop.run_until_complete(init(model_id))
    print(init_result)
    detail_id = init_result[0][0]
    spr_detail_id = init_result[0][1]
    if detail_id:
        post_result = loop.run_until_complete(past_init(request, model_id, spr_detail_id, detail_id))
        options = post_result[4][0]
        captions = post_result[4][1]
        subcaptions = post_result[4][2]
        values = post_result[4][3]
        detail_name = post_result[5][0]
    else:
        post_result = loop.run_until_complete(past_init(request, model_id, None, None))
        options = None
        captions = None
        subcaptions = None
        values = None
        detail_name = None
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
    model = post_result[0][0]
    model_main_image = post_result[0][1]
    model_images = post_result[0][2]
    brand_id = post_result[0][3]
    brand_name = post_result[0][4]
    modules = post_result[1][0]
    cur_module = post_result[1][1]
    partcatalog = post_result[1][2]
    verrors = post_result[2]
    cartridges = post_result[3]
    # print(datetime.datetime.now() - start_time, 'завершение')
    if model_id:
        return render(request, 'model/index.html',
                      {'detail_id': detail_id, 'model': model, 'model_main_image': model_main_image, 'modules': modules,
                       'verrors': verrors, 'model_images': model_images, 'detail_name': detail_name, 'options': options,
                       'partcatalog': partcatalog, 'captions': captions, 'brand_id': brand_id, 'brand_name': brand_name,
                       'subcaptions': subcaptions, 'values': values, 'cur_module': cur_module,
                       'cartridges': cartridges})
    else:
        raise Http404('Страница отсутствует, с id: ' + str(detail_id))




