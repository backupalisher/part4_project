from rest_framework import serializers
from db_model.models import Cartridge


class CartridgeCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Cartridge
        fields = '__all__'


class CartridgeListSerialize(serializers.ModelSerializer):
    class Meta:
        model = Cartridge
        fields = ('id', 'code')
