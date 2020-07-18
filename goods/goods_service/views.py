from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from goods_service.models import Advert as AdvertModel
from goods_service.serializers import AdvertSerializer, AdvertBriefSerializer


class Advert(ModelViewSet):
    queryset = AdvertModel.objects.all()
    serializer_class = AdvertSerializer

    def retrieve(self, request, pk=None):
        adv = get_object_or_404(self.queryset, pk=pk)
        adv.increment_views()
        return Response(self.serializer_class(adv).data)


class AdvertBrief(ReadOnlyModelViewSet):
    queryset = AdvertModel.objects.all()
    serializer_class = AdvertBriefSerializer
