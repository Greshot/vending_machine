from decimal import Decimal
from django.forms import ValidationError
import pytest

from apps.vending.tests.factories.product import ProductFactory
from contextlib import nullcontext as do_not_raises


@pytest.mark.django_db()
class TestProduct:
    @pytest.mark.parametrize(
        "attributes, exception",
        [
            (
                {"name": "Wrong priced product", "price": Decimal("-1.5")},
                pytest.raises(ValidationError),
            ),
            (
                {"name": "Good priced product", "price": Decimal("10.40")},
                do_not_raises(),
            ),
        ],
    )
    def test_product_creation_validations(self, attributes, exception):
        product = ProductFactory(name=attributes["name"], price=attributes["price"])

        with exception as exc:
            product.full_clean()
