from rest_framework import serializers
from db_model.models import Partcodes


class SuppliesCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Partcodes
        fields = '__all__'


class SuppliesListSerialize(serializers.ModelSerializer):
    class Meta:
        model = Partcodes
        fields = ('id', 'code')
