from unittest.mock import ANY
import pytest
from rest_framework import status
from apps.vending.tests.factories.user import UserFactory


@pytest.mark.django_db
class TestVendingMachineSlots:
    def test_list_slot_returns_expected_response(self, client, slots_grid):
        user = UserFactory()
        client.force_authenticate(user=user)
        response = client.get("/slots/")

        expected_response = [
            {
                "id": ANY,
                "quantity": 0,
                "coordinates": [1, 1],
                "product": {"id": ANY, "name": "Product 10", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 1,
                "coordinates": [2, 1],
                "product": {"id": ANY, "name": "Product 9", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 2,
                "coordinates": [3, 1],
                "product": {"id": ANY, "name": "Product 8", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 3,
                "coordinates": [4, 1],
                "product": {"id": ANY, "name": "Product 7", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 4,
                "coordinates": [5, 1],
                "product": {"id": ANY, "name": "Product 6", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 0,
                "coordinates": [1, 2],
                "product": {"id": ANY, "name": "Product 5", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 1,
                "coordinates": [2, 2],
                "product": {"id": ANY, "name": "Product 4", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 2,
                "coordinates": [3, 2],
                "product": {"id": ANY, "name": "Product 3", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 3,
                "coordinates": [4, 2],
                "product": {"id": ANY, "name": "Product 2", "price": "10.40"},
            },
            {
                "id": ANY,
                "quantity": 4,
                "coordinates": [5, 2],
                "product": {"id": ANY, "name": "Product 1", "price": "10.40"},
            },
        ]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response
