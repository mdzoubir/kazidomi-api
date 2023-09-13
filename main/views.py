from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.generics import ListCreateAPIView


from main.models import Product
from main.serializers import ProductSerializer


# Create your views here.
class ProductList(APIView):

    # def get_queryset(self):
    #     return super().get_queryset()

    def get(self, request):
        queryset = Product.objects.select_related('category', 'vendor').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because a instanced of orderitem '})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)