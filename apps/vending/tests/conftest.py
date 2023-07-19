import pytest
from apps.vending.models import Product, VendingMachineSlot
from apps.vending.tests.factories.product import ProductFactory
from apps.vending.tests.factories.vending_machine_slot import VendingMachineSlotFactory
from rest_framework.test import APIClient


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def products_list() -> list[Product]:
    return [ProductFactory(name=f"Product {i}") for i in range(1, 11)]


@pytest.fixture
def slots_grid(products_list) -> list[VendingMachineSlot]:
    """returns a grid of slots of 5x2"""
    slots = []
    for row in range(1, 3):
        for column in range(1, 6):
            slot = VendingMachineSlotFactory(
                product=products_list.pop(), row=row, column=column, quantity=column - 1
            )
            slots.append(slot)

    return slots
