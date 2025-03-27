from rest_framework import serializers
from django.utils import timezone
from ..models import PurchaseDetail, PurchaseHeader, Item


class PurchaseDetailSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(write_only=True)  # Untuk menerima item_code dari request

    class Meta:
        model = PurchaseDetail
        fields = ['item_code', 'quantity', 'unit_price']

    def create(self, validated_data):
        """Ambil header_code dari context, cari item & header, lalu buat PurchaseDetail."""
        header_code = self.context.get('header_code')  

        if not header_code:
            raise serializers.ValidationError({"header_code": "Missing header_code in URL path."})

        item_code = validated_data.pop("item_code")  

        item = Item.objects.filter(code=item_code).first()
        if not item:
            raise serializers.ValidationError({"item_code": "Invalid item_code, item not found."})

        header = PurchaseHeader.objects.filter(code=header_code).first()
        if not header:
            raise serializers.ValidationError({"header_code": "Invalid header_code, purchase header not found."})

        purchase_detail = PurchaseDetail.objects.create(item=item, header=header, **validated_data)

        item.stock += purchase_detail.quantity
        item.balance += purchase_detail.quantity * purchase_detail.unit_price
        item.save()

        return purchase_detail


class PurchaseDetailListSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(source="item.code", read_only=True)
    item_name = serializers.CharField(source="item.name", read_only=True)
    header_code = serializers.CharField(source="header.code", read_only=True)

    class Meta:
        model = PurchaseDetail
        fields = ['header_code', 'item_code', 'item_name', 'quantity', 'unit_price', 'created_at', 'updated_at']
