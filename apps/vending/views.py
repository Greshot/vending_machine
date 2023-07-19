from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.db import transaction
from apps.vending.exceptions import OrderException

from apps.vending.models import VendingMachineSlot, Wallet
from apps.vending.serializers import SlotSerializer, WalletSerializer
from apps.vending.validators import WalletValidator, OrderValidator

class VendingMachineSlotView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        slots = VendingMachineSlot.objects.all()
        slots_serializer = SlotSerializer(slots, many=True)

        return Response(data=slots_serializer.data)
    
class WalletView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        wallet_serializer = WalletSerializer(wallet)

        return Response(data=wallet_serializer.data)
    
    def post(self, request: Request):
        validator = WalletValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        request_dto = validator.build_dto()
        
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        wallet.balance += request_dto.amount
        wallet.save()

        return Response(status=HTTP_200_OK)
    
class OrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        validator = OrderValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        order_items = validator.build_dto()
        item_ids = []
        items_by_id = {}
        for order_item in order_items:
            item_ids.append(order_item.id)
            items_by_id[order_item.id] = order_item

        slots = VendingMachineSlot.objects.filter(id__in=item_ids)
        wallet = Wallet.objects.get(user=request.user)
        
        
        validation_error = False
        errors = []
        try:
            with transaction.atomic():
                order_price = 0
                for slot in slots:
                    item_quantity = items_by_id[slot.id].quantity
                    if(slot.quantity < item_quantity):
                        errors.append(f"There are only {slot.quantity} {slot.product.name}, and you are trying to buy {item_quantity}")
                        print("Appending error 1")
                    else:
                        slot.quantity -= item_quantity
                        slot.save()
                        order_price += slot.product.price * item_quantity

                if(wallet.balance < order_price):
                    errors.append(f"You don't have enough money to complete the order")
                    print("Appending error 2")

                if not errors:
                    wallet.balance -= order_price
                    wallet.save()
                else:
                    raise OrderException() # Raise custom exception to cause the transaction rollback
        except OrderException as ex:
            validation_error= True


        if(validation_error):
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    "error": True,
                    "errors": errors,
                   
                }
            )

        return Response(
            data={
                "error": False, 
                "message": "order processed successfully. Enjoy your products!"
            }, 
            status=HTTP_200_OK
        )

