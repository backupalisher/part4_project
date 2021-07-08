from rest_framework import generics

from db_model.models import Partcodes
from .serializers import SuppliesCreateSerialize, SuppliesListSerialize


class SupplieCreateView(generics.CreateAPIView):
    serializer_class = SuppliesCreateSerialize


class SupplieListView(generics.ListAPIView):
    serializer_class = SuppliesListSerialize
    queryset = Partcodes.objects.filter(supplies=True)


class SupplieEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SuppliesCreateSerialize
    queryset = Partcodes.objects.filter(supplies=True)
