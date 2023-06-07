from django.shortcuts import render
from .models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = User.objects.filter(email=email).first()

    if user is None:
        raise AuthenticationFailed("User not found.")

    if not user.check_password(password):
        raise AuthenticationFailed("Incorrect password.")

    if not user.is_active:
        raise AuthenticationFailed("Confirm your email.")

    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])


    token = TokenObtainPairSerializer.get_token(user)
    
    try:
        group = user.groups.all().first().name    
    except:
        group = None

    response = Response(
        {
            "refresh": str(token),
            "access": str(token.access_token),
            "group": group      
        },
        status=status.HTTP_200_OK,
    )
    return response
