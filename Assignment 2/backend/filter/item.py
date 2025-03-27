import django_filters
from django.db.models import Q  
from ..models import *

class ItemFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Item
        fields = ['search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(code__icontains=value) | Q(name__icontains=value) | Q(unit__icontains=value)
        )
