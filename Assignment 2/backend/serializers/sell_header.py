from rest_framework import serializers
from django.utils import timezone
from ..models import SellHeader


class SellHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellHeader
        fields = ['code', 'date', 'description']

    def delete(self, instance):
        instance.deleted_at = timezone.now()
        instance.deleted_by = self.context['request'].user
        instance.is_deleted = True
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()
        instance.updated_by = self.context['request'].user
        instance.save()
        return instance

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['created_at'] = timezone.now()
        return SellHeader.objects.create(**validated_data)


class SellHeaderListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellHeader
        fields = '__all__'
