from decimal import Decimal
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Product(models.Model):
    class Meta:
        db_table = "product"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=4, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class VendingMachineSlot(models.Model):
    class Meta:
        db_table = "vending_machine_slot"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    row = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    column = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    def __str__(self):
        return f"Product: {self.product.name}, quantity: {self.quantity}, row: {self.row}, column: {self.column}"


class Wallet(models.Model):
    class Meta:
        db_table = "wallet"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    updated_at = models.DateTimeField(auto_now=True)
