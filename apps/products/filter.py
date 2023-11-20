import django_filters
from .models import Product

class NearestProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(lookup_expr='gte')
    max_price = django_filters.NumberFilter(lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name','min_price', 'max_price']
