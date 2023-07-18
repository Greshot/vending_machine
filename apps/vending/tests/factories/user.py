from factory.django import DjangoModelFactory

from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    id = 1
    username = "UserName"
    first_name = "FirstName"
    last_name = "FirstName"
    email = "Email"
    password = "Password"
    