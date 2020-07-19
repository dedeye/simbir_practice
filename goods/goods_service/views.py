from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from goods_service.serializers import AdvertSerializer, AdvertBriefSerializer, AdvertTagSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from goods_service.models import Advert as AdvertModel,\
    AdvertTag as AdvertTagModel

from rest_framework import pagination


class Advert(ModelViewSet):
    queryset = AdvertModel.objects.all()

    detailed_actions = {'create', 'destroy',
                        'retrieve', 'update',
                        'partial_update'}

    def get_serializer_class(self):
        if self.action in self.detailed_actions:
            return AdvertSerializer
        else:
            return AdvertBriefSerializer

    @action(detail=True)
    def brief(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        adv = get_object_or_404(self.queryset, pk=pk)
        adv.increment_views()

        return Response(self.get_serializer(adv).data)

    by_tag_param = openapi.Parameter('tag',
                                     in_=openapi.IN_QUERY,
                                     type=openapi.TYPE_ARRAY,
                                     items={'type': 'string'},
                                     collectionFormat="multi")

    @swagger_auto_schema(manual_parameters=[by_tag_param])
    @action(detail=False)
    def by_tag(self, request, *args, **kwargs):
        tags = self.request.query_params.getlist('tag', None)
        if tags is not None:
            queryset = self.queryset.filter(tags__name__in=tags)

        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=False, methods=['get'])
    def all_tags(self, request, *args, **kwargs):
        class TagPagination(pagination.PageNumberPagination):
            page_size = 30

        tag_paginator = TagPagination()

        tags = AdvertTagModel.objects.all()
        page = tag_paginator.paginate_queryset(tags, request=request)

        if page is not None:
            serializer = AdvertTagSerializer(page, many=True)
            return tag_paginator.get_paginated_response(serializer.data)

        serializer = AdvertTagSerializer(page, many=True)
