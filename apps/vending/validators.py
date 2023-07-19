from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from rest_framework import serializers

@dataclass(frozen=True)
class WalletDTO:
    amount: Decimal

class WalletValidator(serializers.Serializer):
    amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=2, min_value=Decimal("0.01"))

    def build_dto(self) -> WalletDTO:
        data = self.validated_data
        return WalletDTO(
            amount=data.get("amount"),
        )
    
@dataclass(frozen=True)
class OrderItemDTO:
    id: UUID
    quantity: int
class OrderItemValidator(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    quantity = serializers.IntegerField(required=True, min_value=1)
class OrderValidator(serializers.Serializer):
    items = OrderItemValidator(many=True)

    def build_dto(self) -> list[OrderItemDTO]:
        return [OrderItemDTO(id=item['id'], quantity=item['quantity']) for item in self.validated_data['items']]
  

