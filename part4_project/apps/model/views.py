from django.shortcuts import render
from django.http import HttpResponse, Http404
import db_model.models as models
from django.db import connections
import datetime

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


async def set_weight(detail_id):
    _query(
        f"UPDATE details SET weight = (w.weight+1) FROM (SELECT weight FROM details WHERE id = {detail_id}) w "
        f"WHERE id = {detail_id}")


async def get_options(detail_id):
    option_vals = _query(f"SELECT sprdo.parent_id, sprdo.id, sprdet.name caption, array_agg(opts.opt_arr) "
                         f"FROM (SELECT d.spr_detail_id, dop.parent_id, concat(sdo.name,': ', spdo.name) opt_arr "
                         f"FROM link_details_options ldo INNER JOIN detail_options dop ON ldo.detail_option_id = dop.id "
                         f"INNER JOIN spr_detail_options sdo ON dop.caption_spr_id = sdo.id "
                         f"INNER JOIN spr_detail_options spdo ON dop.detail_option_spr_id = spdo.id "
                         f"INNER JOIN details d ON d.id = ldo.detail_id WHERE ldo.detail_id = {detail_id} "
                         f"ORDER BY dop.id DESC) opts "
                         f"LEFT JOIN detail_options sprdo on opts.parent_id = sprdo.id "
                         f"LEFT JOIN spr_detail_options sprdet on sprdet.id = sprdo.detail_option_spr_id "
                         f"LEFT JOIN spr_details sd on sd.id = opts.spr_detail_id "
                         f"GROUP BY sprdet.name, sprdo.parent_id, sprdo.id, sd.name ORDER BY id asc;")
    print(datetime.datetime.now() - start_time, 'получение опций')

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
    print(datetime.datetime.now() - start_time, 'сортировка опций')

    return options


async def get_errors(detail_id):
    verrors = _query(
        f"SELECT m.id mid, m.name, ec.code, ec.display, secd.text description, secc.text causes, secr.text remedy "
        f"FROM models m  LEFT JOIN link_model_error_code lmec ON lmec.model_id = m.id "
        f"LEFT JOIN error_code ec ON ec.id = lmec.error_code_id "
        f"LEFT JOIN spr_error_code secd ON secd.id = ec.description_id "
        f"LEFT JOIN spr_error_code secc ON secc.id = ec.causes_id "
        f"LEFT JOIN spr_error_code secr ON secr.id = ec.remedy_id WHERE m.id = {detail_id}")

    print(datetime.datetime.now() - start_time, 'получение ошибок')
    if len(verrors) > 0:
        if verrors[0][2] is None and verrors[0][3] is None and verrors[0][4] is None and verrors[0][5] is None:
            verrors = None
    print(datetime.datetime.now() - start_time, 'сортировка ошибок')
    return verrors


async def qet_partcatalog(request, model_id):
    partcatalog = _query(f'SELECT m.name model_name, m.image model_picture, m.main_image model_scheme, ' \
                         f'mo.name module_name, mo.name_ru module_name_ru, mo.description module_desc, ' \
                         f'mo.scheme_picture module_picture, p.description code_desc, p.code partcode, ' \
                         f'p.images code_image, sd.name detail_name, sd.name_ru detail_name_ru, ' \
                         f'sd.desc detail_desc, sd.seo detail_seo, sd.base_img detail_img, d.id ' \
                         f'FROM details d ' \
                         f'left JOIN spr_modules mo on d.module_id = mo.id ' \
                         f'LEFT JOIN partcodes p on d.partcode_id = p.id ' \
                         f'LEFT JOIN models m on d.model_id = m.id ' \
                         f'LEFT JOIN spr_details sd on d.spr_detail_id = sd.id ' \
                         f'WHERE d.model_id = {model_id} ORDER BY mo.name')

    print(datetime.datetime.now() - start_time)

    # 'Получение id парткодов, моделей, модулей, названий детали для модулей и парткаталога', q_code_module)
    modules = []
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
    print(datetime.datetime.now() - start_time, 'Сортировка парткаталога')

    return modules, cur_module, partcatalog


def index(request, detail_id):
    print(start_time, 'start')

    # Запрос на добавление веса
    set_weight(detail_id)
    print(datetime.datetime.now() - start_time, 'обновление веса')
    try:
        set_weight(detail_id).run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

    # Запрос на получение ошибок
    verrors = get_errors(detail_id)

    # Запрос на получение опций и вывод опций
    options = get_options(detail_id)

    # Получение id парткодов, моделей, модулей, названий детали для модулей и парткаталога
    try:
        try:
            partcode_id = models.Details.objects.filter(id=detail_id).values('partcode_id')[0]['partcode_id']
            partcode = models.Partcodes.objects.filter(id=partcode_id).values('code')[0]['code']
        except:
            partcode = '-'
        try:
            model_id = models.Details.objects.filter(id=detail_id).values('model_id')[0]['model_id']
            model = models.Models.objects.filter(id=model_id).values('name')[0]['name']
        except:
            model = '-'
        try:
            model_main_image = models.Models.objects.filter(id=model_id).values('main_image')[0]['main_image']
        except:
            model_main_image = False
        try:
            model_images = models.Models.objects.filter(id=model_id).values('image')[0]['image'].split(';')[: - 1]
        except:
            model_images = False
        try:
            module_id = models.Details.objects.filter(id=detail_id).values('module_id')[0]['module_id']
            module = models.Modules.objects.filter(id=module_id).values('name')[0]['name']
        except:
            module = '-'
        try:
            spr_detail_id = models.Details.objects.filter(id=detail_id).values('spr_detail_id')[0]['spr_detail_id']
            if models.Spr_details.objects.filter(id=spr_detail_id).values('name_ru')[0]['name_ru'] != None:
                detail_name = models.Spr_details.objects.filter(id=spr_detail_id).values('name_ru')[0]['name_ru']
            else:
                detail_name = models.Spr_details.objects.filter(id=spr_detail_id).values('name')[0]['name']
        except:
            detail_name = '-'
        brand_id = models.Models.objects.filter(id=model_id).values('brand_id')[0]['brand_id']
        brand_name = models.Brands.objects.filter(id=brand_id).values('name')[0]['name']
        print(datetime.datetime.now() - start_time, 'Запрос на получение парткодов и модулей')

        # Запрос на получение парткодов и модулей

        modules, cur_module, partcatalog = qet_partcatalog(request, model_id)

    except:
        raise Http404('Страница отсутствует, с id: ' + str(detail_id))

    return render(request, 'model/index.html',
                  {'partcode': partcode, 'detail_id': detail_id, 'model': model, 'module': module,
                   'model_main_image': model_main_image, 'modules': modules, 'verrors': verrors,
                   'model_images': model_images, 'detail_name': detail_name, 'options': options,
                   'partcatalog': partcatalog, 'captions': captions, 'brand_id': brand_id, 'brand_name': brand_name,
                   'subcaptions': subcaptions, 'values': values, 'cur_module': cur_module})
