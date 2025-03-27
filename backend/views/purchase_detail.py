from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import PurchaseDetail, PurchaseHeader
from ..serializers.purchase_detail import PurchaseDetailSerializer, PurchaseDetailListSerializer


class PurchaseDetailListView(generics.ListAPIView):
    serializer_class = PurchaseDetailListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        header_code = self.kwargs.get("header_code")

        try:
            header = PurchaseHeader.objects.get(code=header_code)
        except PurchaseHeader.DoesNotExist:
            return Response({"error": "Header not found"}, status=status.HTTP_404_NOT_FOUND)

        details = PurchaseDetail.objects.filter(header=header)
        details_data = PurchaseDetailListSerializer(details, many=True).data

        response_data = {
            "code": header.code,
            "date": header.date.strftime("%Y-%m-%d"),
            "description": header.description,
            "details": details_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class PurchaseDetailCreateView(generics.CreateAPIView):
    serializer_class = PurchaseDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["header_code"] = self.kwargs.get("header_code")  
        return context

    @swagger_auto_schema(
        request_body=PurchaseDetailSerializer,
        responses={201: PurchaseDetailSerializer, 400: "Validation Error"},
        manual_parameters=[
            openapi.Parameter(
                'header_code',
                openapi.IN_PATH,
                description="Kode header dari purchase order",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        header_code = self.kwargs.get("header_code")
        try:
            header = PurchaseHeader.objects.get(code=header_code)
        except PurchaseHeader.DoesNotExist:
            return Response({"error": "Header not found"}, status=status.HTTP_404_NOT_FOUND)

        details = PurchaseDetail.objects.filter(header=header)
        details_data = PurchaseDetailListSerializer(details, many=True).data

        response_data = {
            "code": header.code,
            "date": header.date.strftime("%Y-%m-%d"),
            "description": header.description,
            "details": details_data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
