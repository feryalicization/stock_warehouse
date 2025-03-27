from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import PurchaseDetail, SellDetail, Item
from ..serializers.report import ReportResponseSerializer
from django.db.models import Sum, F, Q
from datetime import datetime

class ItemReportView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: ReportResponseSerializer()},
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
        ]
    )
    def get(self, request, item_code, *args, **kwargs):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if not start_date or not end_date:
            return Response({"error": "Both start_date and end_date are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format, use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Item.objects.get(code=item_code)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        purchases = PurchaseDetail.objects.filter(
            item=item,
            header__date__range=[start_date, end_date]
        ).order_by("header__date")

        sales = SellDetail.objects.filter(
            item=item,
            header__date__range=[start_date, end_date]
        ).order_by("header__date")

        transactions = []
        stock_qty = []
        stock_price = []
        stock_total = []
        balance_qty = 0
        balance = 0

        for purchase in purchases:
            stock_qty.append(purchase.quantity)
            stock_price.append(purchase.unit_price)
            stock_total.append(purchase.quantity * purchase.unit_price)

            balance_qty += purchase.quantity
            balance += purchase.quantity * purchase.unit_price

            transactions.append({
                "date": purchase.header.date,
                "description": purchase.header.description,
                "code": purchase.header.code,
                "in_qty": purchase.quantity,
                "in_price": purchase.unit_price,
                "in_total": purchase.quantity * purchase.unit_price,
                "out_qty": 0,
                "out_price": 0,
                "out_total": 0,
                "stock_qty": stock_qty.copy(),
                "stock_price": stock_price.copy(),
                "stock_total": stock_total.copy(),
                "balance_qty": balance_qty,
                "balance": balance
            })

        for sale in sales:
            if balance_qty < sale.quantity:
                return Response({"error": "Not enough stock for sale"}, status=status.HTTP_400_BAD_REQUEST)

            out_price = stock_price[0] if stock_price else 0
            out_total = sale.quantity * out_price

            stock_qty[0] -= sale.quantity
            if stock_qty[0] == 0:
                stock_qty.pop(0)
                stock_price.pop(0)
                stock_total.pop(0)

            balance_qty -= sale.quantity
            balance -= out_total

            transactions.append({
                "date": sale.header.date,
                "description": sale.header.description,
                "code": sale.header.code,
                "in_qty": 0,
                "in_price": 0,
                "in_total": 0,
                "out_qty": sale.quantity,
                "out_price": out_price,
                "out_total": out_total,
                "stock_qty": stock_qty.copy(),
                "stock_price": stock_price.copy(),
                "stock_total": stock_total.copy(),
                "balance_qty": balance_qty,
                "balance": balance
            })

        summary = {
            "in_qty": sum(p.quantity for p in purchases),
            "out_qty": sum(s.quantity for s in sales),
            "balance_qty": balance_qty,
            "balance": balance
        }

        response_data = {
            "items": transactions,
            "item_code": item.code,
            "name": item.name,
            "unit": item.unit,
            "summary": summary
        }

        return Response({"result": response_data}, status=status.HTTP_200_OK)
