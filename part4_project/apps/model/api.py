from rest_framework import generics

from db_model.models import Models
from .serializers import ModelsCreateSerialize, ModelsListSerialize


class ModelsCreateView(generics.CreateAPIView):
    serializer_class = ModelsCreateSerialize


class ModelsListView(generics.ListAPIView):
    serializer_class = ModelsListSerialize
    queryset = Models.objects.all()


class ModelsEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ModelsCreateSerialize
    queryset = Models.objects.all()
