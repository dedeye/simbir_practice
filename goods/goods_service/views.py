from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, views, generics
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from goods_service.serializers import (
    AdvertSerializer,
    AdvertBriefSerializer,
    AdvertTagSerializer,
    AdvertImageSerializer,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from django.shortcuts import get_object_or_404
from goods_service.models import (
    Advert as AdvertModel,
    AdvertTag as AdvertTagModel,
    AdvertImage as AdvertImageModel,
)

from rest_framework import pagination
from rest_framework.exceptions import ValidationError
import dateutil.parser
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser

from rest_framework import status


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

    by_tag_param = openapi.Parameter(
        "tag",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_ARRAY,
        items={"type": "string"},
        collectionFormat="multi",
    )

    @action(detail=True)
    def brief(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    @swagger_auto_schema(manual_parameters=[by_tag_param])
    @action(detail=False)
    def by_tag(self, request, *args, **kwargs):
        tags = self.request.query_params.getlist("tag", None)
        if tags is not None:
            queryset = self.queryset.filter(tags__name__in=tags)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(self.get_serializer(queryset, many=True).data)

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

    max_param = openapi.Parameter(
        "max", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
    )

    min_param = openapi.Parameter(
        "min", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
    )

    sort_price_types = {"lowest": "price", "highest": "-price"}
    sort_price_param = openapi.Parameter(
        "sort",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        enum=list(sort_price_types.keys()),
    )

    @swagger_auto_schema(manual_parameters=[max_param, min_param, sort_price_param])
    @action(detail=False)
    def by_price(self, request, *args, **kwargs):
        max = self.request.query_params.get("max", 2147483647)
        min = self.request.query_params.get("min", 0)
        sort = self.request.query_params.get("sort", "lowest")

        if sort not in self.sort_price_types.keys():
            raise ValidationError("sort not supported")

        queryset = self.queryset.filter(price__gte=min, price__lte=max).order_by(
            self.sort_price_types[sort]
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(self.get_serializer(queryset, many=True).data)

    after_param = openapi.Parameter(
        "after",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        format=openapi.FORMAT_DATETIME,
        default="2020-07-19T00:00:00Z",
    )

    before_param = openapi.Parameter(
        "before",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        format=openapi.FORMAT_DATETIME,
        default="2020-07-19T00:00:00Z",
    )

    sort_date_types = {"newest": "-created", "oldest": "created"}
    sort_date_param = openapi.Parameter(
        "sort",
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        enum=list(sort_date_types.keys()),
    )

    @swagger_auto_schema(manual_parameters=[after_param, before_param, sort_date_param])
    @action(detail=False)
    def by_date(self, request, *args, **kwargs):
        before = self.request.query_params.get("before", "3000-01-01T00:00:00")
        after = self.request.query_params.get("after", "0001-01-01T00:00:00")
        sort = self.request.query_params.get("sort", "newest")

        # print('reverse ', reverse('goods:advert-img', args=[1,2]))
        # print('reverse ', self.img.url_name)
        if sort not in self.sort_date_types.keys():
            raise ValidationError("sort not supported")

        try:
            before = dateutil.parser.parse(before)
            after = dateutil.parser.parse(after)
        except (Exception):
            raise ValidationError("can not parse date")

        queryset = self.queryset.filter(
            created__range=[str(after), str(before)]
        ).order_by(self.sort_date_types[sort])

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(self.get_serializer(queryset, many=True).data)

    # @action(
    #     detail=True,
    #     methods=["get", "put", "delete"],
    #     url_path="image/(?P<img_id>[^/.]+)",
    # )
    # def img(self, request, *args, **kwargs):
    #     advert = self.get_object()
    #     queryset = AdvertImageModel.objects.filter(advert__id=advert.id)
    #     return Response(self.get_serializer(queryset, many=True).data)

    # @action(detail=True, methods=["post"])
    # def img_upload(self, request, *args, **kwargs):
    #     # parser_classes = [MultiPartParser]
    #     serializer_class = AdvertImageSerializer

    #     queryset = AdvertImageModel.objects.all()
    #     print(request.data)

    #     # serializer_class = AdvertImageSerializer

    #     # def post(self, request, advert, format=None):
    #     if "file" not in request.data:
    #         raise ValidationError("Empty content")

    #     f = request.data["file"]
    #     adv = self.get_object()
    #     AdvertImageModel.objects.create(advert=adv, file=f)

    #     return Response(status=status.HTTP_201_CREATED)


# class AdvertImageView(mixins.RetrieveModelMixin, generics.CreateAPIView):
#     parser_classes = [MultiPartParser]
#     queryset = AdvertImageModel.objects.all()

#     # serializer_class = AdvertImageSerializer

#     def post(self, request, advert, format=None):
#         if "file" not in request.data:
#             raise ValidationError("Empty content")

#         f = request.data["file"]
#         adv = AdvertModel.objects.get(id=advert)
#         AdvertImageModel.objects.create(advert=adv, file=f)

#         return Response(status=status.HTTP_201_CREATED)


class AdvertImageView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
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
