import json

from decouple import config

from django.shortcuts import render
from django.db.models import query, Avg

from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


from products.models import Seller, Product, ProductComment, SellerComment, ProductRating, SellerRating
from products.serializers import (
    SellerSerializer, ProductSerializer, ProductCommentSerializer, SellerCommentSerializer,
    ProductRatingSerializer, SellerRatingSerializer
)
from products.filter import NearestProductFilter

from products.paginators import ProductPageNumberPaginator



def search_products_view(request):
    return render(request, 'products/search_products.html')

# def products_page(request):
#     return render(request, 'products.html')

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

# class NearestProductViewSet(ListAPIView):
#     serializer_class = ProductSerializer
#     filter_backends = [OrderingFilter]
#     # filterset_class = NearestProductFilter
    
    

#     def get_queryset(self):
#         user_latitude = float(self.request.query_params.get('latitude'))
#         user_longitude = float(self.request.query_params.get('longitude'))

#         queryset = Product.objects.all()
#         nearest_products = []

#         for product in queryset:
#             seller = product.seller
#             distance = ((user_latitude - seller.latitude) ** 2 + (user_longitude - seller.longitude) ** 2) ** 0.5
#             nearest_products.append((product, distance))

        
#         nearest_products.sort(key=lambda x: x[0].price)

        
#         nearest_products.sort(key=lambda x: x[1])

        
#         return [product for product, _ in nearest_products]

class NearestProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NearestProductFilter
    pagination_class = ProductPageNumberPaginator


    def list(self, request):
        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))

        queryset = Product.objects.all()
        nearest_products = []


        for product in queryset:
            seller = product.seller
            distance = ((user_latitude - seller.latitude) ** 2 + (user_longitude - seller.longitude) ** 2) ** 0.5
            nearest_products.append({
                'name': product.name,
                'seller_latitude': seller.latitude,
                'seller_longitude': seller.longitude,
                'distance': distance,
                'product': ProductSerializer(product).data,
                'comments': ProductCommentSerializer(ProductComment.objects.filter(product=product), many=True).data,
                'ratings': ProductRatingSerializer(ProductRating.objects.filter(product=product), many=True).data,
                'average_rating': ProductRating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0.0,
            })

        nearest_products.sort(key=lambda x: x['distance'])

        serialized_products = []

        # for product, distance, seller in nearest_products:
        #     product_data = ProductSerializer(product).data
        #     comments = ProductComment.objects.filter(product=product)
        #     ratings = ProductRating.objects.filter(product=product)
        #     average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
        #     product_data['comments'] = ProductCommentSerializer(comments, many=True).data
        #     product_data['ratings'] = ProductRatingSerializer(ratings, many=True).data
        #     product_data['average_rating'] = average_rating if average_rating else 0.0
        #     product_data['seller_latitude'] = seller.latitude
        #     product_data['seller_longitude'] = seller.longitude
        #     serialized_products.append(product_data)
        


        context = {'nearest_products': json.dumps(nearest_products), 
                   'products': nearest_products,
                   'mapkey' : config('MAP_KEY', str)
                   }
        return render(request, 'products/products.html', context)

        # return Response({'products': serialized_products}, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

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
    


