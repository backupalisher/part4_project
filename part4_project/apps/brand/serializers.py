from rest_framework import serializers
from db_model.models import Brands


class BrandCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'


class BrandListSerialize(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ('id', 'name')
