from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import CustomUser


class RegistrationSerializer(ModelSerializer):

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"

    password = serializers.CharField(
        max_length=40,
        min_length=6,
        write_only=True
    )

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=30, read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        fields = ["email", "password"]

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email is None:
            raise serializers.ValidationError(
                "Ожидается Email"
            )

        if password is None:
            raise serializers.ValidationError(
                "Ожидается пароль"
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "Пользователь с таким паролем не найден"
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Данного пользователя не существует или он удален."
            )

        return {
            "email": user.email,
            "token": user.token,
            "id": user.id
        }



