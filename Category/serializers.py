from rest_framework import serializers
from wagtail.fields import StreamValue
from .models import ProductCategory  


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(read_only =True)
    slug = serializers.CharField(read_only=True)
    cate_title = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def serialize_streamfield(self, streamfield_value):
        if isinstance(streamfield_value, StreamValue):
            return [block.get_prep_value() for block in streamfield_value]
        return streamfield_value
class CategoryDetailSerializer(CategorySerializer):
    products = serializers.SerializerMethodField()
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
