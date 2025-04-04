from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from user_auth.models import User, EmailVerificationToken


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model during registration and profile management.
    Handles user creation with password hashing and default role.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'is_verified']
        extra_kwargs = {
            'password': {'write_only': True},  # Password not included in responses
            'role': {'read_only': True},       # Prevent clients from setting role
            'is_verified': {'read_only': True} # Prevent clients from setting verification status
        }

    def create(self, validated_data):
        """
        Custom create method to hash password and set default role.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.role = 'job_seeker'  # Default role as per your model
        user.is_verified = False  # Default as per your model
        user.is_active = False    # Inactive until verified (for your RegisterView)
        user.save()
        return user

class EmailVerificationTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for EmailVerificationToken model.
    Used to validate and display token details during email verification.
    """
    class Meta:
        model = EmailVerificationToken
        fields = ['user', 'token', 'created_at', 'expires_at']
        extra_kwargs = {
            'user': {'read_only': True},    # User is set automatically
            'token': {'read_only': True},   # Token is auto-generated
            'created_at': {'read_only': True},  # Auto-set
            'expires_at': {'read_only': True}   # Auto-set
        }


# Authentication Serializers
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.role = 'job_seeker'  # Default role from your model
        user.is_verified = False  # Default from your model
        user.is_active = False  # Inactive until verified (for email verification)
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    class Meta:
        model = User
        fields = ['password','username','tokens']
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = auth.authenticate(username=username,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')