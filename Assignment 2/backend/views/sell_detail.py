from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import SellDetail, SellHeader
from ..serializers.sell_detail import SellDetailSerializer, SellDetailListSerializer


class SellDetailListView(generics.ListAPIView):
    serializer_class = SellDetailListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        header_code = self.kwargs.get("header_code")

        try:
            header = SellHeader.objects.get(code=header_code)
        except SellHeader.DoesNotExist:
            return Response({"error": "Header not found"}, status=status.HTTP_404_NOT_FOUND)

        details = SellDetail.objects.filter(header=header)
        details_data = SellDetailListSerializer(details, many=True).data

        response_data = {
            "code": header.code,
            "date": header.date.strftime("%Y-%m-%d"),
            "description": header.description,
            "details": details_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SellDetailCreateView(generics.CreateAPIView):
    serializer_class = SellDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["header_code"] = self.kwargs.get("header_code")
        return context

    @swagger_auto_schema(
        request_body=SellDetailSerializer,
        responses={201: "Sell detail successfully created", 400: "Validation Error"},
        manual_parameters=[
            openapi.Parameter(
                "header_code",
                openapi.IN_PATH,
                description="Kode header dari Sell order",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        header_code = kwargs.get("header_code")

        try:
            header = SellHeader.objects.get(code=header_code)
        except SellHeader.DoesNotExist:
            return Response({"error": "Header not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        details = SellDetail.objects.filter(header=header)
        details_data = SellDetailListSerializer(details, many=True).data

        response_data = {
            "code": header.code,
            "date": header.date.strftime("%Y-%m-%d"),
            "description": header.description,
            "details": details_data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
