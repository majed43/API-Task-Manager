from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import (
    EmailAuthTokenSerializer,
    UserSerializer,
    UserUpdatePassword,
    UserUpdateProfile,
)


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    token, _ = Token.objects.get_or_create(user=serializer.instance)
    return Response(
        {"user": serializer.data, "token": token.key}, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search(request, username):
    try:
        user = User.objects.filter(username__contains=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserUpdateProfile(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user
    serializer = UserUpdatePassword(instance=user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    Token.objects.filter(user=serializer.instance).delete()
    token = Token.objects.create(user=serializer.instance)
    return Response(
        {"detail": "Password updated successfully", "token": token.key},
        status=status.HTTP_200_OK,
    )


class EmailAuthToken(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        headers = self.get_success_headers(serializer.data)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "message": "User registered successfully",
                "user": serializer.data,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
