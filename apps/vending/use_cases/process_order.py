from django.contrib.auth.models import User
from django.db import transaction
from apps.vending.exceptions import OrderException
from apps.vending.models import VendingMachineSlot, Wallet
from apps.vending.validators import OrderItemDTO


class ProcessOrder:
    def execute(self, order_items: list[OrderItemDTO], user: User):
        item_ids = []
        items_by_id = {}
        for order_item in order_items:
            item_ids.append(order_item.id)
            items_by_id[order_item.id] = order_item

        slots = VendingMachineSlot.objects.filter(id__in=item_ids)
        wallet = Wallet.objects.get(user=user)

        errors = []
        try:
            with transaction.atomic():
                order_price = 0
                for slot in slots:
                    item_quantity = items_by_id[slot.id].quantity
                    if slot.quantity < item_quantity:
                        errors.append(
                            f"There are only {slot.quantity} {slot.product.name}, and you are trying to buy {item_quantity}"
                        )
                    else:
                        slot.quantity -= item_quantity
                        slot.save()
                        order_price += slot.product.price * item_quantity

                if wallet.balance < order_price:
                    errors.append(f"You don't have enough money to complete the order")
                else:
                    wallet.balance -= order_price
                    wallet.save()

                if errors:
                    raise OrderException()  # Raise custom exception to cause the transaction rollback
        except OrderException as ex:
            pass

        return errors
