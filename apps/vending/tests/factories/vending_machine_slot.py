from datetime import datetime
from decimal import Decimal
import random
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from apps.vending.models import VendingMachineSlot
from apps.vending.tests.factories.product import ProductFactory


class VendingMachineSlotFactory(DjangoModelFactory):
    class Meta:
        model = VendingMachineSlot

    id = Faker("uuid4")
    product = SubFactory(ProductFactory)
    quantity = random.randint(1, 10)
