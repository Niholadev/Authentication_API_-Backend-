
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        user = User(
        username=self.initial_data.get('username'),
        email=self.initial_data.get('email')
        )
        
        validate_password(value, user)
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid username or password."
            )

        attrs['user'] = user
        return attrs



