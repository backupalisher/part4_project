from django.shortcuts import render
from django.http import HttpResponse, Http404
import db_model.models as models
from django.db import connections


def detail_view(request):
    return render(request, 'detail/index.html')

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
    q_options = "SELECT sprdo.parent_id, sprdo.id, sprdet.name caption, array_agg(opts.opt_arr) FROM (SELECT d.spr_detail_id, dop.parent_id, concat(sdo.name,': ', spdo.name) opt_arr FROM link_details_options ldo INNER JOIN detail_options dop ON ldo.detail_option_id = dop.id INNER JOIN spr_detail_options sdo ON dop.caption_spr_id = sdo.id INNER JOIN spr_detail_options spdo ON dop.detail_option_spr_id = spdo.id INNER JOIN details d ON d.id = ldo.detail_id WHERE ldo.detail_id = %d ORDER BY dop.id DESC) opts LEFT JOIN detail_options sprdo on opts.parent_id = sprdo.id LEFT JOIN spr_detail_options sprdet on sprdet.id = sprdo.detail_option_spr_id LEFT JOIN spr_details sd on sd.id = opts.spr_detail_id GROUP BY sprdet.name, sprdo.parent_id, sprdo.id, sd.name ORDER BY id asc;" % (detail_id)
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
            module_id = models.Details.objects.filter(id=detail_id).values('module_id')[0]['module_id']
            module = models.SprModules.objects.filter(id=module_id).values('name')[0]['name']
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
        try:
            model_d_id = models.Details.objects.filter(model_id=model_id).filter(module_id__isnull=True).values('id')[0]['id']
        except:
            model_d_id = 0
        brand_id = models.Models.objects.filter(id=model_id).values('brand_id')[0]['brand_id']
        brand_name = models.Brands.objects.filter(id=brand_id).values('name')[0]['name']
        # Запрос на получение парткодов и модулей
        q_code_module = "SELECT m.name model_name, m.image model_picture, m.main_image model_scheme, mo.name module_name, mo.description module_desc, mo.scheme_picture module_picture, p.description code_desc, p.code partcode, p.images code_image, sd.name detail_name, sd.name_ru detail_name_ru, sd.desc detail_desc, sd.seo detail_seo, sd.base_img detail_img FROM details d left JOIN spr_modules mo on d.module_id = mo.id LEFT JOIN partcodes p on d.partcode_id = p.id LEFT JOIN models m on d.model_id = m.id LEFT JOIN spr_details sd on d.spr_detail_id = sd.id WHERE d.model_id =%d" % (
                model_id)
        option_vals = _query(q_options)
        captions = []
        subcaptions = []
        values = []
        for opts in option_vals:
            if opts[0] is None and opts[1] is None:
                for i in range(len(opts[3])):
                    opts[3][i] = opts[3][i].replace('Caption: ','')
                captions.append(opts)
            if opts[0] is None and opts[1] is not None:
                for opt in opts[3]:
                    if 'SubCaption' in opt:
                        opts[3].remove(opt)
                subcaptions.append(opts)
            else:
                values.append(opts)
        # print(captions)
        # print(subcaptions)
        # print(values)
        options = option_vals
        partcatalog = _query(q_code_module)
    except:
        raise Http404('Страница отсутствует, с id: ' + str(detail_id))

    return render(request, 'detail/index.html',
                  {'partcode': partcode, 'detail_id': detail_id, 'model': model, 'model_id': model_id,
                   'module': module, 'model_d_id': model_d_id, 'detail_name': detail_name, 'options': options,
                   'partcatalog': partcatalog, 'captions': captions, 'subcaptions': subcaptions, 'values': values,
                   'brand_id': brand_id, 'brand_name': brand_name})
