from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now

class BaseModels(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)s_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)s_updated_by")
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)s_deleted_by")

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        """Soft delete instead of hard deleting"""
        self.deleted_at = now()
        self.save()

    def restore(self):
        """Restore the soft-deleted record"""
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        """Check if the record is soft-deleted"""
        return self.deleted_at is not None

    class Meta:
        abstract = True


class Item(BaseModels, SoftDeleteModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class PurchaseHeader(BaseModels, SoftDeleteModel):
    code = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code


class PurchaseDetail(BaseModels):
    header = models.ForeignKey(PurchaseHeader, on_delete=models.CASCADE, related_name="details")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="purchases")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        """Update item stock and balance when a purchase is made."""
        if not self.pk:  
            self.item.stock += self.quantity
            self.item.balance += self.quantity * self.unit_price
            self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"


class SellHeader(BaseModels, SoftDeleteModel):
    code = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code


class SellDetail(BaseModels):
    header = models.ForeignKey(SellHeader, on_delete=models.CASCADE, related_name="details")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="sells")
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        """Update item stock and balance when a sale is made."""
        if not self.pk:  
            if self.item.stock >= self.quantity:
                self.item.stock -= self.quantity
                self.item.save()
            else:
                raise ValueError("Not enough stock available")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"
