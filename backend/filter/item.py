import django_filters
from ..models import Item

class ItemFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Item
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            django_filters.models.Q(code__icontains=value) |
            django_filters.models.Q(name__icontains=value) |
            django_filters.models.Q(unit__icontains=value)
        )
