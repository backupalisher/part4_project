from django.shortcuts import render
from django.http import HttpResponse, Http404
import db_model.models as models

def detail_view(request):
    return render(request, 'detail/index.html')


def index(request, detail_id):
    try:
        try:
            partcode_id = models.Details.objects.filter(id=detail_id).values('partcode_id')[0]['partcode_id']
            partcode = models.Partcodes.objects.filter(id=partcode_id).values('code')[0]['code']
            print(partcode)
        except:
            partcode = '-'
        try:
            model_id = models.Details.objects.filter(id=detail_id).values('model_id')[0]['model_id']
            model = models.Models.objects.filter(id=model_id).values('name')[0]['name']
            print(model)
        except:
            model = '-'
        try:
            module_id = models.Details.objects.filter(id=detail_id).values('module_id')[0]['module_id']
            module = models.Modules.objects.filter(id=module_id).values('name')[0]['name']
            print(module)
        except:
            module = '-'
        try:
            spr_detail_id = models.Details.objects.filter(id=detail_id).values('detail_id')[0]['detail_id']
            detail_name = models.Spr_details.objects.filter(id=spr_detail_id).values('name')[0]['name']
            print(detail_name)
        except:
            detail_name = '-'

    except:
        raise Http404('Страница отсутствует, с id: ' + str(partcode))
    return render(request, 'detail/index.html', {'partcode': partcode, 'detail_id': detail_id, 'model': model, 'module': module, 'detail_name': detail_name})
