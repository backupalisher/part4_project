from rest_framework import generics, response
from db_model.models import Brands
from .serializers import BrandCreateSerialize, BrandListSerialize


class BrandCreateView(generics.CreateAPIView):
    serializer_class = BrandCreateSerialize


class BrandListView(generics.ListAPIView):
    serializer_class = BrandListSerialize
    queryset = Brands.objects.all()


class BrandEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BrandCreateSerialize
    queryset = Brands.objects.all()
