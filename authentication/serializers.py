from rest_framework import serializers
from .models import User
from malaria import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'user_name', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}


class RegisteredPersonnelSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = ['user_name', 'email', 'role',
                  'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            user_name=self.validated_data['user_name'],
            email=self.validated_data['email']

        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "Password mismatch"})
        user.set_password(password)
        user.role = self.validated_data['role']
        user.save()
        models.RegisteredPersonnel.objects.create(user=user)
        return user


class HospitalSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = ['user_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            user_name=self.validated_data['user_name'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "Password mismatch"})
        user.set_password(password)
        user.role = "hospital"
        user.save()
        models.Hospital.objects.create(user=user)
        return user


class AdminSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = ['user_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            user_name=self.validated_data['user_name'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "Password mismatch"})
        user.set_password(password)
        user.role = "admin"
        user.is_verified = True
        user.save()
        models.RegisteredPersonnel.objects.create(user=user)
        return user
