from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from user_auth.models import User, EmailVerificationToken, PasswordResetToken


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

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email exists.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    def validate_token(self, value):
        if not PasswordResetToken.objects.filter(token=value).exists():
            raise serializers.ValidationError("Invalid or expired token.")
        return value


# Authentication Serializers
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    role = serializers.ChoiceField(choices=User.ROLES, default='job_seeker')  # Allow role selection

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        role = attrs.get('role', 'job_seeker')

        if not username.isalnum():
            raise serializers.ValidationError({"username": "Username must be alphanumeric"})

        # Optional: Restrict 'admin' role during registration
        if role == 'admin':
            raise serializers.ValidationError({"role": "Admin role cannot be selected during registration"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role'],  # Set the chosen role
            is_verified=False,
            is_active=False  # Inactive until verified
        )
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
            raise serializers.ValidationError("Invalid or expired refresh token")