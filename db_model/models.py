from django.db import models

# Create your models here.
class Brands(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    logotype = models.CharField(max_length=255)

    class Meta:
        db_table = 'spr_details'

class Cartridge(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    code =  models.CharField(max_length=255)
    analogs = models.TextField()
    techs = models.TextField()
    brand_id = models.ForeignKey('Brands', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'cartridge'

class Details(models.Model):
    id = models.IntegerField(primary_key=True)
    partcode_id = models.IntegerField()
    model_id = models.IntegerField()
    module_id = models.IntegerField()
    detail_id = models.IntegerField()

    class Meta:
        db_table = 'details'

class DetailOptions(models.Model):
    id = models.IntegerField(primary_key=True)
    caption_spr_id = models.IntegerField()
    detail_option_spr_id = models.IntegerField()
    parent_id = models.IntegerField()
    icon = models.CharField(max_length=255)
    value = models.IntegerField()

    class Meta:
        db_table = 'detail_options'

class FilterSettings(models.Model):
    id = models.IntegerField(primary_key=True)
    caption = models.CharField(max_length=255)
    subcaption = models.CharField(max_length=255)
    sub_id = models.IntegerField()
    type = models.CharField(max_length=255)
    values = models.TextField()
    caption_en = models.CharField(max_length=255)
    subcaption_en = models.CharField(max_length=255)
    main_filter = models.IntegerField()

    class Meta:
        db_table = 'filter_settings'

class LinkDetailsOptions(models.Model):
    detail_id = models.IntegerField()
    detail_option_id = models.IntegerField()
    spr_details_id = models.IntegerField()

    class Meta:
        db_table = 'link_details_options'

class LinkModelModules(models.Model):
    model_id = models.IntegerField()
    module_id = models.IntegerField()

    class Meta:
        db_table = 'link_model_modules'

class Models(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    brand_id = models.IntegerField()
    scheme_picture = models.TextField()
    picture = models.TextField()

    class Meta:
        db_table = 'models'

class Modules(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1500)
    scheme_picture = models.CharField(max_length=255)

    class Meta:
        db_table = 'modules'

class Partcodes(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.TextField()
    description = models.TextField()
    images = models.CharField(max_length=1500)

    class Meta:
        db_table = 'partcodes'

class SprDetailOptions(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    class Meta:
        db_table = 'spr_detail_options'

class Spr_details(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    name_ru = models.TextField()
    desc = models.TextField()
    seo = models.TextField()
    base_img = models.CharField(max_length=1500)

    class Meta:
        db_table = 'spr_details'

