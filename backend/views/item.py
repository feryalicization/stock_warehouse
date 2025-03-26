from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from ..models import Item
from ..serializers.item import ItemSerializer, ItemListDetailSerializer
from ..filter.item import ItemFilter

class ItemCreateView(generics.CreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ItemListView(generics.ListAPIView):
    queryset = Item.objects.filter(deleted_at__isnull=True)
    serializer_class = ItemListDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ItemDetailView(generics.RetrieveAPIView):
    serializer_class = ItemListDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        code = self.kwargs.get("code")
        return generics.get_object_or_404(Item.objects.filter(deleted_at__isnull=True), code=code)


class ItemUpdateDeleteAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        code = self.kwargs.get("code")
        return generics.get_object_or_404(Item.objects.filter(deleted_at__isnull=True), code=code)

    def destroy(self, request, *args, **kwargs):
        """Soft delete an item by setting `deleted_at`."""
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.deleted_by = request.user
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "Item soft deleted."}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """Update an item."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
