from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from main.models import Product, Category
from main.serializers import ProductSerializer, CategorySerializer


# Create your views here.
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('category', 'vendor').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CategoryList(ListCreateAPIView):
    queryset = Category.objects.annotate(products_count=Count('products')).all()
    serializer_class = CategorySerializer


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # change the delete method whe have
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because a instanced of orderitem '})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(products_count=Count('products')).all()
    serializer_class = CategorySerializer

    # change the delete method whe have
    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'Category cannot be deleted because a instanced of product '})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)