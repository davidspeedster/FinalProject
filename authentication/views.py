from rest_framework import generics, permissions, status, request
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
import coreapi
from .custom_permissions import isAdmin
from rest_framework.schemas import AutoSchema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class AuthViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field('desc')
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class PersonnelSignupView(generics.GenericAPIView):
    schema = AuthViewSchema()

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisteredPersonnelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": serializers.UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "account created successfully"
        })


class HospitalSignupView(generics.GenericAPIView):
    schema = AuthViewSchema()

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.HospitalSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": serializers.UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "account created successfully"
        })


class AdminSignupView(generics.GenericAPIView):
    schema = AuthViewSchema()

    permission_classes = [permissions.IsAuthenticated & isAdmin]
    serializer_class = serializers.AdminSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": serializers.UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "account created successfully"
        })


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'role': user.role
        })


class LogoutAPIView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)
