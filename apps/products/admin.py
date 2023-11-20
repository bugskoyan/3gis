from django.contrib import admin

from products.models import Seller, Product, SellerRating, SellerComment, ProductComment, ProductRating

admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(SellerComment)
admin.site.register(ProductComment)
admin.site.register(SellerRating)
admin.site.register(ProductRating)

