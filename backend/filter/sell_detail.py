import django_filters
from ..models import SellDetail

class SellDetailFilter(django_filters.FilterSet):
    header_code = django_filters.CharFilter(field_name='header__code', lookup_expr='icontains', label='Search by Header Code')
    item_name = django_filters.CharFilter(field_name='item__name', lookup_expr='icontains', label='Search by Item Name')
    quantity = django_filters.NumberFilter(field_name='quantity', lookup_expr='exact', label='Search by Quantity')

    class Meta:
        model = SellDetail
        fields = ['header_code', 'item_name', 'quantity']
