from rest_framework import serializers
from db_model.models import Partcodes


class DetailsCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Partcodes
        depth = 1
        fields = '__all__'
        # fields = ('id', 'partcode_id', 'model_id', 'module_id', 'spr_detail_id')


class DetailsListSerialize(serializers.ModelSerializer):
    class Meta:
        model = Partcodes
        fields = '__all__'
        # fields = ('id', 'partcode_id.code', 'model_id.name', 'module_id.name', 'spr_detail_id.name')
