from rest_framework import generics

from db_model.models import Partcodes
from .serializers import DetailsCreateSerialize, DetailsListSerialize


class DetailsCreateView(generics.CreateAPIView):
    serializer_class = DetailsCreateSerialize


class DetailsListView(generics.ListAPIView):
    serializer_class = DetailsListSerialize
    queryset = Partcodes.objects.all()


class DetailsEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailsCreateSerialize
    queryset = Partcodes.objects.all()
