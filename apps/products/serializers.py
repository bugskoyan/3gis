from rest_framework import serializers
from .models import Seller, Product, SellerComment, SellerRating, ProductComment, ProductRating

class SellerSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    poster: str = serializers.ImageField()
    description = serializers.CharField()
    
    class Meta:
        model = Seller
        fields = ['name','latitude','longitude','poster','description']

    


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    seller = serializers.StringRelatedField()
    poster: str = serializers.ImageField()
    description = serializers.CharField()

    class Meta:
        model = Product
        fields = ['name','price','seller','poster','description']

    
        

class ProductCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ProductComment
        fields = '__all__'


class SellerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerComment
        fields = '__all__'


class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    class Meta:
        model = ProductRating
        fields = '__all__'


class SellerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerRating
        fields = '__all__'







 