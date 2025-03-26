import django_filters
from ..models import PurchaseDetail

class PurchaseDetailFilter(django_filters.FilterSet):
    header_code = django_filters.CharFilter(field_name='header__code', lookup_expr='icontains', label='Search by Header Code')
    item_name = django_filters.CharFilter(field_name='item__name', lookup_expr='icontains', label='Search by Item Name')
    quantity = django_filters.NumberFilter(field_name='quantity', lookup_expr='exact', label='Search by Quantity')
    unit_price = django_filters.NumberFilter(field_name='unit_price', lookup_expr='exact', label='Search by Unit Price')

    class Meta:
        model = PurchaseDetail
        fields = ['header_code', 'item_name', 'quantity', 'unit_price']
