from rest_framework import serializers
from wagtail.fields import StreamValue
from .models import ProductPage
from wagtail import blocks 
from wagtail.images.blocks import ImageChooserBlock
from wagtail.rich_text import RichText
from Gmart.utils import get_image_rendition
from django.conf import settings
#import pdb; pdb.set_trace() debugggg
# class ProductPageSerializer(serializers.Serializer):
#     title = serializers.CharField(read_only=True)
#     slug = serializers.CharField(read_only=True)
#     content = serializers.ListField(child=serializers.DictField(), read_only=True)
class ProductPageSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_title', read_only=True)
    related_products = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    class Meta:
        model = ProductPage
        # fields = '__all__'
        fields = ['id', 'title', 'content', 'category','related_products','images']
    
    def get_images(self, instance):
        images_data = []
        for block in instance.content:
            if isinstance(block, StreamValue):
                for detail_block in block:
                    if detail_block.block_type == 'product_details':
                        image_blocks = detail_block.value.get('images', [])
                        for image_block in image_blocks:
                            image_data = self.get_image(image_block)
                            if image_data:
                                images_data.append(image_data)
        return images_data
    def get_image(self, image_block):
        if image_block:
            rendition = get_image_rendition(image_block, 'original')  # Modify based on your image fetching logic
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": image_block.alt if image_block.alt else ''
                }
        return None
    def get_category_title(self, instance):
        for block in instance.content:
            if isinstance(block, StreamValue):
                for detail_block in block:
                    if detail_block.block_type == 'product_details':
                        category_page = detail_block.value.get('category')
                        return category_page.title if category_page else None
        return None

    def get_related_products(self, instance):
        category_title = self.get_category_title(instance)
        if category_title:
            related_products = ProductPage.objects.filter(
                content__product_details__category__title=category_title  
            ).exclude(id=instance.id) 
            return ProductPageSerializer(related_products, many=True).data
        return []
    def to_representation(self, instance):
        # print(instance)
        try:
            representation = super().to_representation(instance)
            # print(representation)
        except Exception as e:
            # print("Error during super call:", str(e))
            raise 
        if hasattr(instance, 'content') and isinstance(instance.content, StreamValue):
            representation['content'] = self.serialize_streamfield(instance.content)
        # print(representation)
        return representation


    def serialize_streamfield(self, streamfield):
        # import pdb; pdb.set_trace()
        if isinstance(streamfield, StreamValue):
            return [self.serialize_block(block) for block in streamfield]
        return []

    def serialize_block(self, block):
        # import pdb; pdb.set_trace()
        # print("Serializing block:", block)
        if isinstance(block, str):
            return {
                'type': 'text',
                'text': block,
            }

        if not hasattr(block, 'value'):
            return {
                'type': 'unknown',
                'value': str(block),
            }

        block_value = block.value
        block_instance = block.block  

        # print("Block instance:", block_instance)
        # print("Type of block_instance:", type(block_instance))

        if isinstance(block_instance, blocks.RichTextBlock):
            rich_text_content = block_value.source if hasattr(block_value, 'source') else str(block_value)
            # print("RichText content:", rich_text_content)
            return {
                'type': 'rich_text',
                'content': rich_text_content,
            }

        elif isinstance(block_instance, ImageChooserBlock):
            image_data = self.get_image(block_value)
            return {
                'type': 'images',
                'url': image_data,
            }

        elif isinstance(block_instance, blocks.CharBlock):
            return {
                'type': 'text',
                'text': block_value,
            }

        elif isinstance(block_instance, blocks.StructBlock):
            serialized_data = {key: self.serialize_block(value) for key, value in block_value.items()}
            return {
                'type': 'struct',
                'fields': serialized_data,
            }

        return {
            'type': 'unknown',
            'value': str(block_value),
        }
    def get_image(self, image_block):
        if image_block:
            rendition = get_image_rendition(image_block, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None



      
        
        
    
#---------------------------------------------------------------------
class ProductPageDetailSerializer(ProductPageSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
