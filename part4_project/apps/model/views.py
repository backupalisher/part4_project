from django.shortcuts import render
from django.http import HttpResponse, Http404
import db_model.models as models
from django.db import connections


def detail_view(request):
    return render(request, 'model/index.html')


def _query(q):
    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.execute(q)
            data = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()
            return data


def index(request, detail_id):
    options = []
    # Запрос на получение опций
    q_options = "SELECT sprdo.parent_id, sprdo.id, sprdet.name caption, array_agg(opts.opt_arr) FROM (SELECT d.spr_detail_id, dop.parent_id, concat(sdo.name,': ', spdo.name) opt_arr FROM link_details_options ldo INNER JOIN detail_options dop ON ldo.detail_option_id = dop.id INNER JOIN spr_detail_options sdo ON dop.caption_spr_id = sdo.id INNER JOIN spr_detail_options spdo ON dop.detail_option_spr_id = spdo.id INNER JOIN details d ON d.id = ldo.detail_id WHERE ldo.detail_id = %d ORDER BY dop.id DESC) opts LEFT JOIN detail_options sprdo on opts.parent_id = sprdo.id LEFT JOIN spr_detail_options sprdet on sprdet.id = sprdo.detail_option_spr_id LEFT JOIN spr_details sd on sd.id = opts.spr_detail_id GROUP BY sprdet.name, sprdo.parent_id, sprdo.id, sd.name ORDER BY id asc;" % (
        detail_id)
    option_vals = _query(q_options)
    #print(option_vals)
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
            model_main_image = '/image/' + models.Models.objects.filter(id=model_id).values('main_image')[0]['main_image']
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
        # Запрос на получение парткодов и модулей
        q_code_module = "SELECT m.name model_name, m.image model_picture, m.main_image model_scheme, mo.name module_name, mo.description module_desc, mo.scheme_picture module_picture, p.description code_desc, p.code partcode, p.images code_image, sd.name detail_name, sd.name_ru detail_name_ru, sd.desc detail_desc, sd.seo detail_seo, sd.base_img detail_img, d.id FROM details d left JOIN spr_modules mo on d.module_id = mo.id LEFT JOIN partcodes p on d.partcode_id = p.id LEFT JOIN models m on d.model_id = m.id LEFT JOIN spr_details sd on d.spr_detail_id = sd.id WHERE mo.name is not null and d.model_id = %d ORDER BY mo.name" % (model_id)
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
        print(q_code_module)
        partcatalog = _query(q_code_module)
        print(partcatalog)
        modules = []
        for parts in partcatalog:
            modules.append(parts[3])
        modules = list(dict.fromkeys(modules))
        if request.GET.get('module'):
            cur_module = request.GET.get('module')
        else:
            cur_module = None
    except:
        raise Http404('Страница отсутствует, с id: ' + str(detail_id))

    return render(request, 'model/index.html',
                  {'partcode': partcode, 'detail_id': detail_id, 'model': model, 'module': module,
                   'model_main_image': model_main_image, 'modules': modules,
                   'model_images': model_images, 'detail_name': detail_name, 'options': options,
                   'partcatalog': partcatalog, 'captions': captions, 'brand_id': brand_id, 'brand_name': brand_name,
                   'subcaptions': subcaptions, 'values': values, 'cur_module': cur_module})
