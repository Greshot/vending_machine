from dataclasses import dataclass
from rest_framework import serializers


@dataclass(frozen=True)
class RegistrationDTO:
    username: str
    email: str
    password: int
    first_name: str | None = None
    last_name: str | None = None


class RegistrationValidator(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=50)
    first_name = serializers.CharField(max_length=150, default=None)
    last_name = serializers.CharField(max_length=150, default=None)

    def build_dto(self) -> RegistrationDTO:
        data = self.validated_data
        return RegistrationDTO(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
        )
