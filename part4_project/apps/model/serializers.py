from rest_framework import serializers
from db_model.models import Models


class ModelsCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Models
        depth = 1
        fields = '__all__'


class ModelsListSerialize(serializers.ModelSerializer):
    class Meta:
        model = Models
        fields = ('id', 'name')
