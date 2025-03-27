from rest_framework import serializers
from ..models import PurchaseDetail, SellDetail, Item

class ReportItemSerializer(serializers.Serializer):
    date = serializers.DateField(format="%d-%m-%Y")
    description = serializers.CharField()
    code = serializers.CharField()
    in_qty = serializers.IntegerField()
    in_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    in_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    out_qty = serializers.IntegerField()
    out_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    out_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    stock_qty = serializers.ListField(child=serializers.IntegerField())
    stock_price = serializers.ListField(child=serializers.DecimalField(max_digits=12, decimal_places=2))
    stock_total = serializers.ListField(child=serializers.DecimalField(max_digits=12, decimal_places=2))
    balance_qty = serializers.IntegerField()
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

class ReportSummarySerializer(serializers.Serializer):
    in_qty = serializers.IntegerField()
    out_qty = serializers.IntegerField()
    balance_qty = serializers.IntegerField()
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

class ReportResponseSerializer(serializers.Serializer):
    items = ReportItemSerializer(many=True)
    item_code = serializers.CharField()
    name = serializers.CharField()
    unit = serializers.CharField()
    summary = ReportSummarySerializer()
