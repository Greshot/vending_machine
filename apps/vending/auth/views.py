from django.db import IntegrityError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from apps.vending.auth.validators import RegistrationValidator

class RegisterUser(APIView):
    
    def post(self, request: Request):
        validator = RegistrationValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        request_dto = validator.build_dto()

        try:
            User.objects.create_user(
                username=request_dto.username, 
                email=request_dto.email, 
                password=request_dto.password, 
                first_name=request_dto.first_name, 
                last_name=request_dto.last_name
            )
        except IntegrityError as ex:
            message = 'Something went wrong'
            if 'UNIQUE constraint failed' in str(ex):
                message = 'Username is already taken. Please use another one'

            return Response(
                data={
                    "error": True, 
                    "message": message
                }, 
                status=HTTP_400_BAD_REQUEST
            )
        
        return Response(
            data={
                "error": False, 
                "message": "User created successfully"
            }, 
            status=HTTP_201_CREATED
        )

class CustomAuthToken(ObtainAuthToken):

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            data={
                'token': token.key,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            },
            status=HTTP_201_CREATED
        )

class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        token = Token.objects.get(user=request.user)
        token.delete()

        return Response(status=HTTP_200_OK)