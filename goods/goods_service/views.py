from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, pagination, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

import dateutil.parser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from goods_service.models import Advert as AdvertModel
from goods_service.models import AdvertImage as AdvertImageModel
from goods_service.models import AdvertTag as AdvertTagModel
from goods_service.serializers import (
    AdvertBriefSerializer,
    AdvertImageSerializer,
    AdvertSerializer,
    AdvertTagSerializer,
)


class AdvertView(ModelViewSet):
    queryset = AdvertModel.objects.all()

    # use detailed presentation in detail view
    detailed_actions = {"create", "destroy", "retrieve", "update", "partial_update"}

    def get_serializer_class(self):
        if self.action in self.detailed_actions:
            return AdvertSerializer
        else:
            return AdvertBriefSerializer

    def retrieve(self, request, pk=None):
        adv = get_object_or_404(self.queryset, pk=pk)
        adv.increment_views()

        return Response(self.get_serializer(adv).data)

    @action(detail=True)
    def brief(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    @action(detail=False)
    def all_tags(self, request, *args, **kwargs):
        class TagPagination(pagination.PageNumberPagination):
            page_size = 30

        tag_paginator = TagPagination()

        tags = AdvertTagModel.objects.all()
        page = tag_paginator.paginate_queryset(tags, request=request)

        if page is not None:
            serializer = AdvertTagSerializer(page, many=True)
            return tag_paginator.get_paginated_response(serializer.data)

        return Response(AdvertTagSerializer(tags, many=True).data)

    # swagger schema for filter
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "before",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
                default="2021-01-01T00:00:00",
            ),
            openapi.Parameter(
                "after",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATETIME,
                default="2020-01-01T00:00:00",
            ),
            openapi.Parameter(
                "max_price", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "min_price", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "tag",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_ARRAY,
                items={"type": "string"},
                collectionFormat="multi",
            ),
            openapi.Parameter(
                "order",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=["cheap", "expensive", "old", "new"],
            ),
        ]
    )
    @action(detail=False)
    def filter(self, request, *args, **kwargs):

        queryset = AdvertModel.objects.all()
        order_types = {
            "cheap": "price",
            "expensive": "-price",
            "old": "created",
            "new": "-created",
        }
        # parse all possible filter params
        before = self.request.query_params.get("before", "3000-01-01T00:00:00")
        after = self.request.query_params.get("after", "0001-01-01T00:00:00")
        max_price = self.request.query_params.get("max_price", None)
        min_price = self.request.query_params.get("min_price", None)
        tags = self.request.query_params.getlist("tag", [])
        order = self.request.query_params.get("order", None)

        # validate order
        if order is not None and order not in order_types.keys():
            raise ValidationError("order type not supported")

        # validate datetime
        try:
            before = dateutil.parser.parse(before)
            after = dateutil.parser.parse(after)
        except (Exception):
            raise ValidationError("can not parse date")

        # filter by tags
        if tags:
            print(tags)
            queryset = queryset.filter(tags__name__in=tags)

        # filter by price
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        # filter by datetime
        queryset = queryset.filter(created__range=[str(after), str(before)])

        # order
        if order is not None:
            queryset = queryset.order_by(order_types[order])

        # paginate
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(self.get_serializer(queryset, many=True).data)


class AdvertImageView(
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet,
):
    parser_classes = [MultiPartParser]
    queryset = AdvertImageModel.objects.all()
    serializer_class = AdvertImageSerializer


class AdvertImageUpload(generics.CreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = AdvertImageSerializer

    def post(self, request, id, format=None):
        if "file" not in request.data:
            raise ValidationError("Empty content")

        f = request.data["file"]
        adv = get_object_or_404(AdvertModel.objects.all(), pk=id)

        AdvertImageModel.objects.create(advert=adv, file=f)

        return Response(status=status.HTTP_201_CREATED)
