from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from wagtail.models import Locale
from django.utils.translation import get_language_from_request
from wagtail.models import Page
from .models import ProductCategory
from Product.models import ProductPage
from .serializers import CategorySerializer, CategoryDetailSerializer
from django.core.paginator import Paginator
PAGINATION_PERPAGE = 10 

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    def get_serializer_class(self):
        group_serializer = {
            'list': CategorySerializer,
            'retrieve': CategoryDetailSerializer,
        }
        serializer_class = group_serializer.get(self.action, None)
        if serializer_class is None:
            raise ValueError(f"No serializer found for action: {self.action}")
        return serializer_class
    def get_queryset(self):
        # try:
        #     category = ProductCategory.objects.get(cate_title='Condiments')
        #     return ProductPage.objects.child_of(category).live()
        # except ProductCategory.DoesNotExist:
        #     return ProductPage.objects.none()
        return ProductCategory.objects.all() 
    def list(self, request, *args, **kwargs):
        response = {}
        try:
            limit = int(request.GET.get('limit', PAGINATION_PERPAGE)) 
            page = int(request.GET.get('page', 1)) 
            querysets = self.get_queryset()
            paginator = Paginator(querysets, limit)
            records = paginator.get_page(page)
            serializer = self.get_serializer(records, many=True, context={'request': request})
            response['result'] = 'success'
            response['records'] = serializer.data
            response['page_count'] = paginator.count
            response['has_next'] = records.has_next()
            response['has_previous'] = records.has_previous()
            response['pages'] = paginator.num_pages
        except Exception as e:
            response['result'] = 'failure'
            response['message'] = str(e)
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        response = {}
        try:
            slug = kwargs.get('slug')
            cate_page = get_object_or_404(self.get_queryset(), slug=slug)
            serializer = self.get_serializer(cate_page, context={'request': request})
            response['result'] = 'success'
            response['records'] = serializer.data
        except Exception as e:
            response['result'] = 'failure'
            response['message'] = str(e)

        return Response(response, status=status.HTTP_200_OK)