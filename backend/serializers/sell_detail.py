from rest_framework import serializers
from django.utils import timezone
from django.core.exceptions import ValidationError
from ..models import SellDetail


class SellDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellDetail
        fields = ['header', 'item', 'quantity']

    def create(self, validated_data):
        item = validated_data['item']
        quantity = validated_data['quantity']
        if item.stock < quantity:
            raise ValidationError("Not enough stock available")

        sell_detail = SellDetail.objects.create(**validated_data)
        item.stock -= quantity
        item.save()

        return sell_detail

    def update(self, instance, validated_data):
        old_quantity = instance.quantity
        new_quantity = validated_data.get('quantity', old_quantity)

        item = instance.item
        stock_change = new_quantity - old_quantity

        if item.stock - stock_change < 0:
            raise ValidationError("Not enough stock available for update")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.updated_at = timezone.now()
        instance.updated_by = self.context['request'].user
        instance.save()
        item.stock -= stock_change
        item.save()

        return instance


class SellDetailListDetailSerializer(serializers.ModelSerializer):
    header_code = serializers.CharField(source='header.code', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = SellDetail
        fields = ['header_code', 'item_name', 'quantity', 'created_at', 'updated_at']
