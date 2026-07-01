from rest_framework import serializers
from .models import CustomUser, EmailOTP


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'username',
            'password',
            'role'
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )

        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class EmailOTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailOTP
        fields = ['email']

class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(max_length=6)