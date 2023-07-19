from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from apps.vending.models import VendingMachineSlot, Wallet
from apps.vending.serializers import SlotSerializer, WalletSerializer
from apps.vending.use_cases.process_order import ProcessOrder
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

        use_case = ProcessOrder()
        errors = use_case.execute(order_items, request.user)

        if errors:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    "error": True,
                    "errors": errors,
                },
            )

        return Response(
            data={
                "error": False,
                "message": "order processed successfully. Enjoy your products!",
            },
            status=HTTP_200_OK,
        )
