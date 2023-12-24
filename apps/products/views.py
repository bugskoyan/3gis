import json

from decouple import config

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import query, Avg
from django.core.paginator import Page, Paginator, EmptyPage
from django.http import Http404

from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination


from products.models import Seller, Product, ProductComment, SellerComment, ProductRating, SellerRating
from products.serializers import (
    SellerSerializer, ProductSerializer, ProductCommentSerializer, SellerCommentSerializer,
    ProductRatingSerializer, SellerRatingSerializer
)
from products.filter import NearestProductFilter
from products.forms import SellerForm, ProductForm,CommentForm, RatingForm

from products.paginators import ProductPageNumberPaginator



def search_products_view(request):
    return render(request, 'products/search_products.html')

# def products_page(request):
#     return render(request, 'products.html')

def add_seller(request):
    user_latitude = request.POST.get('latitude')
    user_longitude = request.POST.get('longitude')

    if request.method == 'POST':
        seller_form = SellerForm(request.POST, request.FILES)
        if seller_form.is_valid():
            seller_form.save()
            return redirect(f'http://127.0.0.1:8000/nearest-products/?latitude={user_latitude}&longitude={user_longitude}')  
    else:
        seller_form = SellerForm()
    
    return render(request, 'products/add-seller.html', {'seller_form': seller_form, 'product_form': ProductForm()})

def add_product(request):
    user_latitude = request.POST.get('latitude')
    user_longitude = request.POST.get('longitude')

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect(f'http://127.0.0.1:8000/nearest-products/?latitude={user_latitude}&longitude={user_longitude}')  
    else:
        product_form = ProductForm()
    
    return render(request, 'products/add-product.html', {'seller_form': SellerForm(), 'product_form': product_form})


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comment_form = CommentForm()
    rating_form = RatingForm()
    
    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.save()
        elif 'rating_submit' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.product = product
                rating.save()

    return render(request, 'products/detail.html', {
        'product': product,
        'comment_form': comment_form,
        'rating_form': rating_form,
    })



class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    def retrieve(self, request, pk=None):
        seller = self.queryset.get(pk=pk)
        seller_products = seller.product_set.all()
        seller_comments = SellerComment.objects.filter(seller=seller)
        seller_ratings = SellerRating.objects.filter(seller=seller)

        product_average_rating = 0.0
        if seller_products.exists():
            product_average_rating = ProductRating.objects.filter(product__in=seller_products).aggregate(Avg('rating'))['rating__avg'] or 0.0
        
        average_rating = seller_ratings.aggregate(Avg('rating'))['rating__avg'] if seller_ratings.exists() else 0.0

        detail_seller = {
            'id': seller.pk,
            'name': seller.name,
            'seller_latitude': seller.latitude,
            'seller_longitude': seller.longitude,
            'seller': SellerSerializer(seller).data,
        }

        return render(request, 'products/seller_detail.html', {
            'seller': seller,
            'detail_seller': json.dumps(detail_seller),
            'id': seller.pk,
            'seller_latitude': seller.latitude,
            'seller_longitude': seller.longitude,
            'seller_products': seller_products,
            'seller_comments': seller_comments,
            'seller_ratings': seller_ratings,
            'average_rating': average_rating,
            'product_average_rating': product_average_rating,
            'mapkey': config('MAP_KEY', str)
        })


# def seller_detail_view(request, seller_id):
#     seller = Seller.objects.get(pk=seller_id)
#     seller_products = Product.objects.filter(seller=seller)

#     return render(request, 'products/seller_detail.html', {'seller': seller, 'seller_products': seller_products})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def add_comment(self, request, pk:int=None):
    #     try:
    #         product = Product.objects.get(pk=pk)
    #         comment_text = request.data.get('text')  
    #         comment = ProductComment.objects.create(product=product, comment=comment_text)

    #         return Response({'message': 'Комментарий успешно добавлен'}, status=status.HTTP_201_CREATED)

    #     except Product.DoesNotExist:
    #         return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)
        
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # def add_rating(self, request, pk=None):
    #     try:
    #         product = Product.objects.get(pk=pk)
    #         rating_value = request.data.get('rating')
    #         rating = ProductRating.objects.create(product=product, rating=rating_value)

    #         return Response({'message': 'Оценка успешно добавлена'}, status=status.HTTP_201_CREATED)

    #     except Product.DoesNotExist:
    #         return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)
        
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NearestProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NearestProductFilter
    pagination_class = ProductPageNumberPaginator
    queryset = Product.objects.all()
    

    def list(self, request):
        user_latitude = float(request.query_params.get('latitude'))
        user_longitude = float(request.query_params.get('longitude'))


        queryset = Product.objects.all()
        nearest_products = []


        for product in queryset:
            seller = product.seller
            distance = ((user_latitude - seller.latitude) ** 2 + (user_longitude - seller.longitude) ** 2) ** 0.5
            nearest_products.append({
                'id' : product.pk,
                'name': product.name,
                'seller_latitude': seller.latitude,
                'seller_longitude': seller.longitude,
                'seller_id' : seller.id,
                'distance': distance,
                'product': ProductSerializer(product).data,
                'comments': ProductCommentSerializer(ProductComment.objects.filter(product=product), many=True).data,
                'ratings': ProductRatingSerializer(ProductRating.objects.filter(product=product), many=True).data,
                'average_rating': ProductRating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0.0,
            })

        nearest_products.sort(key=lambda x: x['distance'])

        serialized_products = []


        latitude = request.query_params.get('latitude', user_latitude)
        longitude = request.query_params.get('longitude', user_longitude)

        paginator = Paginator(nearest_products, self.pagination_class.page_size)
        page_number = request.query_params.get(self.pagination_class.page_query_param, 1)

        try:
            page = paginator.page(page_number)
        except EmptyPage as e:
            raise Http404("Invalid page number") from e

        serialized_page = [
            {
                'id': item['id'],
                'name': item['name'],
                'seller_latitude': item['seller_latitude'],
                'seller_longitude': item['seller_longitude'],
                'distance': item['distance'],
                'product': item['product'],
                'comments': item['comments'],
                'ratings': item['ratings'],
                'average_rating': item['average_rating'],
            }
            for item in page.object_list
        ]


        context = {'nearest_products': json.dumps(nearest_products), 
                   'products': nearest_products,
                   'mapkey' : config('MAP_KEY', str),
                   'products_page' : page
                   }
        return render(request, 'products/products.html', context)

        # return Response({'products': serialized_products}, status=status.HTTP_200_OK)


    
    def retrieve(self, request, pk=None):
        
        try:
            product = self.queryset.get(pk=pk)
            seller = product.seller
            detail_product = {
                'id': product.pk,
                'name': product.name,
                'seller_latitude': seller.latitude,
                'seller_longitude': seller.longitude,
                'seller_id' : seller.id,
                'product': ProductSerializer(product).data,
                'comments': ProductCommentSerializer(ProductComment.objects.filter(product=product), many=True).data,
                'ratings': ProductRatingSerializer(ProductRating.objects.filter(product=product), many=True).data,
                'average_rating': ProductRating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0.0,
            }
        except Product.DoesNotExist:
            return Response({"error": "Нет такого товара"}, status=status.HTTP_404_NOT_FOUND)

        context = {
            'detail_product': json.dumps(detail_product),
            'product': detail_product,
            'mapkey': config('MAP_KEY', str)
        }
        return render(request, 'products/detail.html', context)
    

    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)

            product.delete()
            return Response({"message": "Продукт успешно удален"}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Нет такого товара"}, status=status.HTTP_404_NOT_FOUND)
    

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
    


