from dataclasses import dataclass
from decimal import Decimal
from rest_framework import serializers

@dataclass(frozen=True)
class WalletDTO:
    amount: Decimal

class WalletValidator(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.01"))

    def build_dto(self) -> WalletDTO:
        data = self.validated_data
        return WalletDTO(
            amount=data.get("amount"),
        )