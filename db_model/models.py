from django.db import models

# Create your models here.
class Details(models.Model):
    id = models.IntegerField(primary_key=True)
    partcode_id = models.IntegerField()
    model_id = models.IntegerField()
    module_id = models.IntegerField()
    detail_id = models.IntegerField()

    class Meta:
        db_table = 'details'

class Partcodes(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.TextField()
    description = models.TextField()
    images = models.CharField(max_length=1500)

    class Meta:
        db_table = 'partcodes'

class Modules(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1500)
    scheme_picture = models.CharField(max_length=255)

    class Meta:
        db_table = 'modules'

class Models(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    brand_id = models.IntegerField()
    scheme_picture = models.TextField()
    picture = models.TextField()

    class Meta:
        db_table = 'models'

class Spr_details(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    name_ru = models.TextField()
    desc = models.TextField()
    seo = models.TextField()
    base_img = models.CharField(max_length=1500)

    class Meta:
        db_table = 'spr_details'