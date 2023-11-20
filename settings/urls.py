from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.products.views import (
    SellerViewSet, ProductViewSet, NearestProductViewSet, ProductCommentViewSet, 
    SellerCommentViewSet,
    ProductRatingViewSet, SellerRatingViewSet, search_products_view
)


router = DefaultRouter()
router.register(r'sellers', SellerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'nearest-products', NearestProductViewSet, basename='nearest-product')
router.register(r'product-comments', ProductCommentViewSet)
router.register(r'seller-comments', SellerCommentViewSet)
router.register(r'product-ratings', ProductRatingViewSet)
router.register(r'seller-ratings', SellerRatingViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('search-products/', search_products_view, name='search_products'),
]