from django.contrib import admin
from django.utils import timezone
from .models import Item, PurchaseHeader, PurchaseDetail, SellHeader, SellDetail


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'deleted_by')
    list_filter = ('deleted_at',)  

    def get_queryset(self, request):
        return super().get_queryset(request).filter(deleted_at__isnull=True)

    def delete_model(self, request, obj):
        obj.deleted_at = timezone.now()
        obj.deleted_by = request.user
        obj.save()


@admin.register(Item)
class ItemAdmin(BaseAdmin):
    list_display = ('code', 'name', 'unit', 'stock', 'balance', 'is_deleted')
    search_fields = ('code', 'name')
    list_filter = ('is_deleted',)


@admin.register(PurchaseHeader)
class PurchaseHeaderAdmin(BaseAdmin):
    list_display = ('code', 'date', 'description', 'is_deleted')
    search_fields = ('code', 'description')
    list_filter = ('is_deleted',)


@admin.register(PurchaseDetail)
class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display = ('header', 'item', 'quantity', 'unit_price')
    search_fields = ('header__code', 'item__name')


@admin.register(SellHeader)
class SellHeaderAdmin(BaseAdmin):
    list_display = ('code', 'date', 'description', 'is_deleted')
    search_fields = ('code', 'description')
    list_filter = ('is_deleted',)


@admin.register(SellDetail)
class SellDetailAdmin(admin.ModelAdmin):
    list_display = ('header', 'item', 'quantity')
    search_fields = ('header__code', 'item__name')
