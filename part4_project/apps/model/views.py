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
    return render(request, '/models/index.html')


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
    verrors = _query(f"SELECT * FROM all_errors WHERE mid = {model_id}  ORDER BY code;")
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


# Получение данных для модели
@sync_to_async
def get_model(model_id):
    return _query(f'SELECT * FROM all_models WHERE model_id = {model_id}')


# Получение данных картриджей
@sync_to_async
def get_cartridge(model_id):
    # print(datetime.datetime.now() - start_time, 'получение картриджей')
    supplies = _query(f"SELECT * FROM all_cartridge WHERE {model_id} = ANY(model_id)")
    for idx in range(len(supplies)):
        supp = list(supplies[idx])
        supp[4] = list(set(supp[4]))
        supplies[idx] = tuple(supp)
        supp_alt = list(supplies[idx])
        supp_alt[8] = list(set(supp[8]))
        supplies[idx] = tuple(supp_alt)
    # print(datetime.datetime.now() - start_time, 'получение картриджей завершено')
    return supplies


async def init(model_id):
    async_tasks = [get_model(model_id)]
    results = await asyncio.gather(*async_tasks)
    return results


async def past_init(request, model_id, detail_id):
    if detail_id:
        tasks = [
            qet_partcatalog(request, model_id),
            get_errors(model_id),
            get_cartridge(model_id),
            get_options(detail_id),
        ]
    else:
        tasks = [
            qet_partcatalog(request, model_id),
            get_errors(model_id),
            get_cartridge(model_id)
        ]
    results = await asyncio.gather(*tasks)
    return results


def index(request, model_id):
    tabs = [
        'options',
        'parts',
        'errors',
        'supplies'
    ]
    tab = request.GET.get('tab')
    # print(start_time, model_id)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    # print(datetime.datetime.now() - start_time, 'start')
    init_result = loop.run_until_complete(init(model_id))[0]
    detail_id = init_result[0][0]
    model_id = init_result[0][1]
    model_name = init_result[0][2]
    model_main_image = init_result[0][3]
    model_images = init_result[0][4]
    brand_id = init_result[0][5]
    brand_name = init_result[0][6]
    type_of_device = [init_result[0][7], init_result[0][8]]
    technology = [init_result[0][9], init_result[0][10]]
    max_format = [init_result[0][11], init_result[0][12]]
    pages_per_month = [init_result[0][13], init_result[0][14]]
    speed = [init_result[0][15], init_result[0][16]]
    output_type = [init_result[0][17], init_result[0][18]]
    loop.create_task(set_weight(detail_id))
    if detail_id:
        post_result = loop.run_until_complete(past_init(request, model_id, detail_id))
        options = post_result[3][0]
        captions = post_result[3][1]
        subcaptions = post_result[3][2]
        values = post_result[3][3]
    else:
        post_result = loop.run_until_complete(past_init(request, model_id, None))
        options = None
        captions = None
        subcaptions = None
        values = None
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
    modules = post_result[0][0]
    cur_module = post_result[0][1]
    partcatalog = post_result[0][2]
    verrors = post_result[1]
    supplies = post_result[2]
    # print(datetime.datetime.now() - start_time, 'завершение')
    if tab:
        pass
    elif cur_module is not None or len(subcaptions) == 0 or tab == 'parts':
        tab = 'parts'
    elif (verrors is not None and len(captions) == 0 and len(modules) == 0) or tab == 'errors':
        tab = 'errors'
    elif (supplies is not None and len(captions) == 0 and len(modules) == 0 and len(verrors) == 0) or tab == 'supplies':
        tab = 'supplies'
    else:
        tab = 'options'
    if model_id:
        return render(request, 'models/index.html',
                      {'detail_id': detail_id, 'model_name': model_name, 'model_main_image': model_main_image,
                       'modules': modules, 'verrors': verrors, 'model_images': model_images, 'options': options,
                       'partcatalog': partcatalog, 'captions': captions, 'brand_id': brand_id, 'brand_name': brand_name,
                       'subcaptions': subcaptions, 'values': values, 'cur_module': cur_module, 'supplies': supplies,
                       'tab': tab, 'type_of_device': type_of_device, 'technology': technology, 'max_format': max_format,
                       'pages_per_month': pages_per_month, 'speed': speed, 'output_type': output_type})
    else:
        raise Http404('Страница отсутствует, с id: ' + str(detail_id))
