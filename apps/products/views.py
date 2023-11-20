from django.shortcuts import render
from django.db.models import query

from rest_framework import permissions
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


from products.models import Seller, Product, ProductComment, SellerComment, ProductRating, SellerRating
from products.serializers import (
    SellerSerializer, ProductSerializer, ProductCommentSerializer, SellerCommentSerializer,
    ProductRatingSerializer, SellerRatingSerializer
)
from products.filter import NearestProductFilter

def search_products_view(request):
    return render(request, 'products/search_products.html')

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

class NearestProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NearestProductFilter
    
    

    def get_queryset(self):
        user_latitude = float(self.request.query_params.get('latitude'))
        user_longitude = float(self.request.query_params.get('longitude'))

        queryset = Product.objects.all()
        nearest_products = []

        for product in queryset:
            seller = product.seller
            distance = ((user_latitude - seller.latitude) ** 2 + (user_longitude - seller.longitude) ** 2) ** 0.5
            nearest_products.append((product, distance))

        # Сортировка по цене (предположим, что у продукта есть поле "price")
        nearest_products.sort(key=lambda x: x[0].price)

        # Затем сортировка по расстоянию
        nearest_products.sort(key=lambda x: x[1])

        
        return [product for product, _ in nearest_products]
    

class ProductCommentViewSet(viewsets.ModelViewSet):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
    

class SellerCommentViewSet(viewsets.ModelViewSet):
    queryset = SellerComment.objects.all()
    serializer_class = SellerCommentSerializer
    

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer
    

class SellerRatingViewSet(viewsets.ModelViewSet):
    queryset = SellerRating.objects.all()
    serializer_class = SellerRatingSerializer
    


