import base64

from rest_framework import serializers

from goods.settings import MEDIA_ROOT
from goods_service.models import Advert, AdvertImage, AdvertTag


class AdvertTagSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        # Perform the data validation.
        if not data:
            raise serializers.ValidationError({"name": "This field is required."})
        if len(data) > 30:
            raise serializers.ValidationError({"name": "May be < 30 chars."})
        return {"name": data}

    def create(self, validated_data):
        return AdvertTag.objects.create(**validated_data)

    def to_representation(self, value):
        return str(value)

    class Meta:
        model = AdvertTag
        fields = "__all__"


class Base64ImageField(serializers.FileField):
    def to_representation(self, value):
        filepath = MEDIA_ROOT + "/" + str(value)
        with open(filepath, "rb") as image_file:
            return image_file.read()


class AdvertImageSerializer(serializers.ModelSerializer):
    file = Base64ImageField()

    class Meta:
        model = AdvertImage
        fields = ["file", "id", "author"]
        read_only_fields = ["id"]


class AdvertSerializer(serializers.ModelSerializer):
    tags = AdvertTagSerializer(many=True)
    image = AdvertImageSerializer(many=True, read_only=True,)

    class Meta:
        model = Advert
        fields = "__all__"
        read_only_fields = ("id", "created", "views")

    def create(self, validated_data):
        tag_list = validated_data.pop("tags")
        adv = Advert.objects.create(**validated_data)

        for tag_data in tag_list:
            tag, _ = AdvertTag.objects.get_or_create(**tag_data)
            adv.tags.add(tag)

        return adv

    def update(self, instance, validated_data):
        tag_list = validated_data.get("tags", None)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.contacts = validated_data.get("contacts", instance.contacts)
        instance.price = validated_data.get("price", instance.price)

        instance.save()

        if tag_list is not None:
            instance.tags.clear()
            for tag_data in tag_list:
                tag, _ = AdvertTag.objects.get_or_create(**tag_data)
                instance.tags.add(tag)

        return instance


class AdvertBriefSerializer(serializers.ModelSerializer):
    detailed = serializers.HyperlinkedIdentityField(view_name="goods:advert-detail")
    tags = AdvertTagSerializer(many=True)

    class Meta:
        model = Advert
        fields = ("id", "title", "price", "views", "detailed", "tags")
