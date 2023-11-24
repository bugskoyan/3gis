from rest_framework import serializers
from .models import Seller, Product, SellerComment, SellerRating, ProductComment, ProductRating

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    seller = serializers.StringRelatedField(
        many=False, 
    )
    poster: str = serializers.ImageField()
    rate: float = serializers.FloatField()
    description = serializers.CharField()
    
        

class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = '__all__'


class SellerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerComment
        fields = '__all__'


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = '__all__'


class SellerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerRating
        fields = '__all__'







 