from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
from ..models import PurchaseDetail, SellDetail, Item
from ..serializers.report import ReportResponseSerializer
from django.db.models import Sum
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ItemReportView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
    responses={
        200: openapi.Response('File PDF atau JSON', openapi.Schema(
            type=openapi.TYPE_FILE
        ))
    },
    manual_parameters=[
        openapi.Parameter(
            'start_date', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", 
            type=openapi.TYPE_STRING, required=True
        ),
        openapi.Parameter(
            'end_date', openapi.IN_QUERY, description="End date (YYYY-MM-DD)", 
            type=openapi.TYPE_STRING, required=True
        ),
        openapi.Parameter(
            'format', openapi.IN_QUERY, description="Response format (json/pdf)", 
            type=openapi.TYPE_STRING, required=False, enum=["json", "pdf"]
        )
    ]
)


    def get(self, request, item_code, *args, **kwargs):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        response_format = request.GET.get("format", "json")

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

        purchases = PurchaseDetail.objects.filter(item=item, header__date__range=[start_date, end_date])
        sales = SellDetail.objects.filter(item=item, header__date__range=[start_date, end_date])

        transactions = []
        balance_qty = 0
        balance = 0

        for purchase in purchases:
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
                "balance_qty": balance_qty,
                "balance": balance
            })

        for sale in sales:
            if balance_qty < sale.quantity:
                return Response({"error": "Not enough stock for sale"}, status=status.HTTP_400_BAD_REQUEST)
            
            balance_qty -= sale.quantity
            balance -= sale.quantity * (balance / balance_qty if balance_qty > 0 else 0)

            transactions.append({
                "date": sale.header.date,
                "description": sale.header.description,
                "code": sale.header.code,
                "in_qty": 0,
                "in_price": 0,
                "in_total": 0,
                "out_qty": sale.quantity,
                "out_price": balance / balance_qty if balance_qty > 0 else 0,
                "out_total": sale.quantity * (balance / balance_qty if balance_qty > 0 else 0),
                "balance_qty": balance_qty,
                "balance": balance
            })

        summary = {
            "in_qty": purchases.aggregate(Sum('quantity'))['quantity__sum'] or 0,
            "out_qty": sales.aggregate(Sum('quantity'))['quantity__sum'] or 0,
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

        if response_format == "pdf":
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.drawString(100, 750, f"Report for {item.name} ({item.code})")
            y_position = 730
            for transaction in transactions:
                pdf.drawString(100, y_position, str(transaction))
                y_position -= 20
            pdf.save()
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{item_code}.pdf"'
            return response

        return Response({"result": response_data}, status=status.HTTP_200_OK)
