from rest_framework import serializers
from ..models import SellDetail, SellHeader, Item


class SellDetailSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(write_only=True)  

    class Meta:
        model = SellDetail
        fields = ['item_code', 'quantity']

    def create(self, validated_data):
        """Process SellDetail creation, update stock and balance."""
        header_code = self.context.get('header_code')  
        if not header_code:
            raise serializers.ValidationError({"header_code": "Missing header_code in URL path."})

        item_code = validated_data.pop("item_code")
        item = Item.objects.filter(code=item_code).first()
        if not item:
            raise serializers.ValidationError({"item_code": "Invalid item_code, item not found."})

        header = SellHeader.objects.filter(code=header_code).first()
        if not header:
            raise serializers.ValidationError({"header_code": "Invalid header_code, Sell header not found."})

        quantity = validated_data.get("quantity")
        if item.stock < quantity:
            raise serializers.ValidationError({"quantity": "Not enough stock available."})

        # Reduce stock & update balance
        item.stock -= quantity
        item.save()

        # Create SellDetail record
        sell_detail = SellDetail.objects.create(item=item, header=header, quantity=quantity)
        return sell_detail


class SellDetailListSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(source="item.code", read_only=True)
    item_name = serializers.CharField(source="item.name", read_only=True)
    header_code = serializers.CharField(source="header.code", read_only=True)

    class Meta:
        model = SellDetail
        fields = ['header_code', 'item_code', 'item_name', 'quantity', 'created_at', 'updated_at']
