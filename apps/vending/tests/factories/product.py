from datetime import datetime
from decimal import Decimal
from factory import Faker
from factory.django import DjangoModelFactory

from apps.vending.models import Product


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    id = Faker("uuid4")
    name = "Snickers Bar"
    price = Decimal("10.40")
    created_at = datetime(2023, 7, 17, 12)
    updated_at = datetime(2023, 7, 17, 23)
    