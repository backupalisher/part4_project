from django.db import models


class Brands(models.Model):
    name = models.CharField(unique=True, max_length=255)
    logotype = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brands'


class DictionaryErrorCode(models.Model):
    text_en = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionary_error_code'


class DictionaryErrorCodeImage(models.Model):
    image = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionary_error_code_image'


class DictionaryModelOptions(models.Model):
    text_en = models.CharField(unique=True, max_length=255, blank=True, null=True)
    text_ru = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionary_model_options'


class DictionaryModuleImage(models.Model):
    image = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionary_module_image'


class DictionaryModules(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name_en = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name_ru = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionary_modules'
        unique_together = (('name_en', 'name_ru'),)


class DictionaryPartcode(models.Model):
    name_en = models.TextField(unique=True, blank=True, null=True)
    name_ru = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionary_partcode'
        unique_together = (('name_en', 'name_ru'),)


class DictionaryPartcodeOptions(models.Model):
    id = models.SmallAutoField(primary_key=True)
    text_en = models.CharField(unique=True, max_length=255)
    text_ru = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionary_partcode_options'


class ErrorCodes(models.Model):
    code = models.IntegerField(blank=True, null=True)
    display = models.IntegerField(blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True)
    description_id = models.IntegerField(blank=True, null=True)
    causes_id = models.IntegerField(blank=True, null=True)
    remedy_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'error_codes'
        unique_together = (('code', 'display', 'image_id', 'description_id', 'causes_id', 'remedy_id'),)


class FilterSettings(models.Model):
    caption = models.CharField(max_length=255, blank=True, null=True)
    subcaption = models.CharField(max_length=255, blank=True, null=True)
    sub = models.ForeignKey(DictionaryModelOptions, models.DO_NOTHING, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    values = models.TextField(blank=True, null=True)  # This field type is a guess.
    caption_en = models.CharField(max_length=255, blank=True, null=True)
    subcaption_en = models.CharField(max_length=255, blank=True, null=True)
    parent_id = models.SmallIntegerField(blank=True, null=True)
    values_en = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'filter_settings'


class LinkDictionaryModelOptions(models.Model):
    dictionary_model_caption_id = models.SmallIntegerField()
    dictionary_model_option_id = models.IntegerField()
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_dictionary_model_options'
        unique_together = (('dictionary_model_caption_id', 'dictionary_model_option_id', 'parent_id'),)


class LinkDictionaryPartcodeOptions(models.Model):
    dictionary_partcode_caption_id = models.SmallIntegerField()
    dictionary_partcode_option_id = models.IntegerField()
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_dictionary_partcode_options'
        unique_together = (('dictionary_partcode_caption_id', 'dictionary_partcode_option_id', 'parent_id'),)


class LinkModelErrorCode(models.Model):
    model = models.ForeignKey('Models', models.DO_NOTHING)
    error_code = models.ForeignKey(ErrorCodes, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_model_error_code'
        unique_together = (('model', 'error_code'),)


class LinkModelModuleImage(models.Model):
    model_id = models.IntegerField()
    dictionary_module_id = models.IntegerField(blank=True, null=True)
    dictionary_module_image_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_model_module_image'
        unique_together = (('model_id', 'dictionary_module_id', 'dictionary_module_image_id'),)


class LinkModelModulePartcode(models.Model):
    partcode = models.ForeignKey('Partcodes', models.DO_NOTHING, blank=True, null=True)
    model = models.ForeignKey('Models', models.DO_NOTHING, blank=True, null=True)
    module = models.ForeignKey(DictionaryModules, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_model_module_partcode'
        unique_together = (('partcode', 'model', 'module'),)


class LinkModelOptions(models.Model):
    model_id = models.IntegerField()
    link_dictionary_model_options_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'link_model_options'


class LinkPartcodeModelAnalogue(models.Model):
    model_id = models.IntegerField(blank=True, null=True)
    partcode_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_partcode_model_analogue'
        unique_together = (('model_id', 'partcode_id'),)


class LinkPartcodeOptions(models.Model):
    partcode_option_id = models.IntegerField()
    partcode_dictionary_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_partcode_options'
        unique_together = (('partcode_option_id', 'partcode_dictionary_id'),)


class Models(models.Model):
    name = models.CharField(unique=True, max_length=255)
    brand_id = models.IntegerField(blank=True, null=True)
    main_image = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'models'


class Partcodes(models.Model):
    code = models.TextField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    article_code = models.TextField(unique=True, blank=True, null=True)
    manufacturer = models.IntegerField(blank=True, null=True)
    dictionary_partcode_id = models.IntegerField(blank=True, null=True)
    supplies = models.BooleanField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partcodes'
        unique_together = (('code', 'manufacturer'),)


class Prices(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vendor = models.ForeignKey('Vendors', models.DO_NOTHING)
    partcode = models.ForeignKey(Partcodes, models.DO_NOTHING, blank=True, null=True)
    model = models.ForeignKey(Models, models.DO_NOTHING, blank=True, null=True)
    usage_status = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    images = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prices'


class Vendors(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendors'
