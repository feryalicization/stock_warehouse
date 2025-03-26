from rest_framework import serializers
from django.utils import timezone
from ..models import PurchaseDetail


class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = ['header', 'item', 'quantity', 'unit_price']

    def create(self, validated_data):
        purchase_detail = PurchaseDetail.objects.create(**validated_data)

        item = purchase_detail.item
        item.stock += purchase_detail.quantity
        item.balance += purchase_detail.quantity * purchase_detail.unit_price
        item.save()

        return purchase_detail

    def update(self, instance, validated_data):
        old_quantity = instance.quantity
        old_unit_price = instance.unit_price

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.updated_at = timezone.now()
        instance.updated_by = self.context['request'].user
        instance.save()

        item = instance.item
        item.stock += instance.quantity - old_quantity
        item.balance += (instance.quantity * instance.unit_price) - (old_quantity * old_unit_price)
        item.save()

        return instance


class PurchaseDetailListDetailSerializer(serializers.ModelSerializer):
    header_code = serializers.CharField(source='header.code', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = PurchaseDetail
        fields = ['header_code', 'item_name', 'quantity', 'unit_price', 'created_at', 'updated_at']
