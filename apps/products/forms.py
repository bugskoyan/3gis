from django import forms
from .models import Seller, Product, ProductComment, ProductRating

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['name', 'latitude', 'longitude', 'poster', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price','seller','poster', 'description']


class CommentForm(forms.Form):
    class Meta:
        model = ProductComment
        # fields = ['user','text']
        widgets = {'text': forms.Textarea}

class RatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['user','rating']