from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ProductPage
from Category.models import  ProductCategory
from .serializers import ProductPageSerializer, ProductPageDetailSerializer
from django.core.paginator import Paginator

PAGINATION_PER_PAGE = 10

class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductPageSerializer

    def get_serializer_class(self):
        group_serializer = {
            'list': ProductPageSerializer,
            'retrieve': ProductPageDetailSerializer,
        }
        return group_serializer.get(self.action, self.serializer_class)

    def get_queryset(self):
    #     return ProductPage.objects.all()
        category_title = self.request.query_params.get('category', None)
        if category_title:
            try:
                category = ProductCategory.objects.get(cate_title__iexact=category_title)
                return ProductPage.objects.child_of(category).live()
            except ProductCategory.DoesNotExist:
                return ProductPage.objects.none()

        return ProductPage.objects.live()
      

    def list(self, request, *args, **kwargs):
        response = {}
        try:
            limit = int(request.GET.get('limit', PAGINATION_PER_PAGE))
            page = int(request.GET.get('page', 1))
            queryset = self.get_queryset()
            if not queryset.exists():
                return Response({"result": "failure", "message": "No products found."}, status=status.HTTP_404_NOT_FOUND)

            paginator = Paginator(queryset, limit)
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
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = {}
        try:
            # slug = kwargs.get('slug')
            product_id = kwargs.get('pk')
            # product_page = get_object_or_404(self.get_queryset(), slug=slug)
            product_page = get_object_or_404(self.get_queryset(),id=product_id)
            serializer = self.get_serializer(product_page, context={'request': request})
            response['result'] = 'success'
            response['records'] = serializer.data
        except ProductPage.DoesNotExist:
            return Response({"result": "failure", "message": "No ProductPage matches the given query."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response['result'] = 'failure'
            response['message'] = str(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)
