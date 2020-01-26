from django.shortcuts import render
from django.http import HttpResponse, Http404
import db_model.models as models
from django.db import connections

def detail_view(request):
    return render(request, 'detail/index.html')


def index(request, detail_id):
    q = "SELECT sdo.id, dop.parent_id, caption.name as caption, sdo.name, sdo.icon, dop.value FROM spr_detail_options " \
        "sdo LEFT JOIN detail_options dop ON sdo.id = dop.detail_option_spr_id LEFT JOIN link_details_options ldo ON " \
        "dop.id = ldo.detail_option_id LEFT JOIN (SELECT sdo.id, sdo.name FROM spr_detail_options sdo " \
        "left JOIN detail_options dop ON sdo.id = dop.caption_spr_id WHERE dop.caption_spr_id IS NOT NULL " \
        "GROUP BY sdo.name, sdo.id ORDER BY sdo.id) caption ON caption.id = dop.caption_spr_id " \
        "WHERE ldo.detail_id = %d ORDER BY sdo.id" % (detail_id)
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


    except:
        raise Http404('Страница отсутствует, с id: ' + str(detail_id))

    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            print(q)
            c.execute(q)
            options = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()

    print(type(options), options)

    return render(request, 'detail/index.html',
                  {'partcode': partcode, 'detail_id': detail_id, 'model': model, 'module': module,
                   'detail_name': detail_name, 'options': options})
