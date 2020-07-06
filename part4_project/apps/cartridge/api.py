from rest_framework import generics

from db_model.models import Cartridge
from .serializers import CartridgeCreateSerialize, CartridgeListSerialize


class CartridgeCreateView(generics.CreateAPIView):
    serializer_class = CartridgeCreateSerialize


class CartridgeListView(generics.ListAPIView):
    serializer_class = CartridgeListSerialize
    queryset = Cartridge.objects.all()


class CartridgeEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartridgeCreateSerialize
    queryset = Cartridge.objects.all()
