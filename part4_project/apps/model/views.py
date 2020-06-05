from django.shortcuts import render
from django.http import HttpResponse, Http404
import db_model.models as models
from django.db import connections
from asgiref.sync import sync_to_async
import datetime
import asyncio
import re
start_time = datetime.datetime.now()


def detail_view(request):
    return render(request, 'model/index.html')


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


# добавление веса
@sync_to_async
def set_weight(detail_id):
    print(datetime.datetime.now() - start_time, 'обновление веса')
    _query(
        f"UPDATE details SET weight = (w.weight+1) FROM (SELECT weight FROM details WHERE id = {detail_id}) w "
        f"WHERE id = {detail_id}")
    print(datetime.datetime.now() - start_time, 'обновление веса завершено')


# Запрос на получение опций и вывод опций
@sync_to_async
def get_options(detail_id):
    captions = []
    subcaptions = []
    values = []
    print(datetime.datetime.now() - start_time, 'получение опций')
    option_vals = _query(f"SELECT * FROM all_options_model WHERE detail_id = {detail_id};")
    print(datetime.datetime.now() - start_time, 'получение опций завершено')

    print(datetime.datetime.now() - start_time, 'сортировка опций')
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
    print(datetime.datetime.now() - start_time, 'сортировка опций завершена')

    return options, captions, subcaptions, values


# Запрос на получение ошибок
@sync_to_async
def get_errors(detail_id):
    print(datetime.datetime.now() - start_time, 'получение ошибок')
    verrors = _query(f"SELECT * FROM all_errors WHERE mid = {detail_id}")
    print(datetime.datetime.now() - start_time, 'получение ошибок завершено')

    print(datetime.datetime.now() - start_time, 'сортировка ошибок')
    if len(verrors) > 0:
        if verrors[0][2] is None and verrors[0][3] is None and verrors[0][4] is None and verrors[0][5] is None:
            verrors = None
    print(datetime.datetime.now() - start_time, 'сортировка ошибок завершена')
    return verrors


# Запрос на получение парткодов и модулей
@sync_to_async
def qet_partcatalog(request, model_id):
    # 'Получение id парткодов, моделей, модулей, названий детали для модулей и парткаталога', q_code_module)
    modules = []
    print(datetime.datetime.now() - start_time, 'получение парткодов и модулей')
    partcatalog = _query(f'SELECT * FROM all_partcatalog WHERE model_id = {model_id}')
    print(datetime.datetime.now() - start_time, 'получение парткодов и модулей завершено')

    print(datetime.datetime.now() - start_time, 'Сортировка парткаталога')
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
    print(datetime.datetime.now() - start_time, 'Сортировка парткаталога завершена')

    return modules, cur_module, partcatalog


# Запрос на получение id
@sync_to_async
def get_ids(detail_id):
    print(datetime.datetime.now() - start_time, 'сбор id')
    qd = _query(f'SELECT * FROM details WHERE id = {detail_id}')
    partcode_id = qd[0][1]
    model_id = qd[0][2]
    module_id = qd[0][3]
    spr_detail_id = qd[0][4]
    print(datetime.datetime.now() - start_time, 'сбор id завершен')
    return model_id, spr_detail_id


# Получение id парткодов, моделей, бренда, картинок
@sync_to_async
def get_any(model_id, spr_detail_id):
    print(datetime.datetime.now() - start_time, 'сбор остального')
    mq = _query(f'SELECT brand_id, name, main_image, image FROM models WHERE id = {model_id}')
    brand_id = mq[0][0]
    model = mq[0][1]
    model_main_image = mq[0][2]
    model_images = mq[0][3]
    dq = _query(f'SELECT name, name_ru FROM spr_details WHERE id = {spr_detail_id}')
    if dq[0][1]:
        detail_name = dq[0][1]
    else:
        detail_name = dq[0][0]
    brand_name = models.Brands.objects.filter(id=brand_id).values('name')[0]['name']
    print(datetime.datetime.now() - start_time, 'сбор остального завершен')
    return model, model_main_image, model_images, detail_name, brand_id, brand_name


async def init(detail_id):
    async_tasks = [get_ids(detail_id)]
    results = await asyncio.gather(*async_tasks)
    return results


async def past_init(request, model_id, spr_detail_id, detail_id):
    tasks = [
        get_any(model_id, spr_detail_id),
        qet_partcatalog(request, model_id),
        get_errors(detail_id),
        get_options(detail_id)
    ]
    results = await asyncio.gather(*tasks)
    return results


def index(request, detail_id):
    print(start_time, detail_id)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.create_task(set_weight(detail_id))
    print(datetime.datetime.now() - start_time, 'start')
    try:
        model_id, spr_detail_id = loop.run_until_complete(get_ids(detail_id))
        post_result = loop.run_until_complete(past_init(request, model_id, spr_detail_id, detail_id))
        model = post_result[0][0]
        model_main_image = post_result[0][1]
        model_images = post_result[0][2]
        detail_name = post_result[0][3]
        brand_id = post_result[0][4]
        brand_name = post_result[0][5]
        modules = post_result[1][0]
        cur_module = post_result[1][1]
        partcatalog = post_result[1][2]
        verrors = post_result[2]
        options = post_result[3][0]
        captions = post_result[3][1]
        subcaptions = post_result[3][2]
        values = post_result[3][3]
    except:
        raise Http404('Страница отсутствует, с id: ' + str(detail_id))
    loop.close()
    print(datetime.datetime.now() - start_time, 'завершение')
    return render(request, 'model/index.html',
                  {'detail_id': detail_id, 'model': model, 'model_main_image': model_main_image, 'modules': modules,
                   'verrors': verrors, 'model_images': model_images, 'detail_name': detail_name, 'options': options,
                   'partcatalog': partcatalog, 'captions': captions, 'brand_id': brand_id, 'brand_name': brand_name,
                   'subcaptions': subcaptions, 'values': values, 'cur_module': cur_module})
