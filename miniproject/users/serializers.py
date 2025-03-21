from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from users.models import User, Profile
from rest_framework import serializers
from .models import Profile


# Authentication Serializers
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = User
        # fields = ['email', 'username', 'password', 'role', 'profile_picture']
        fields = ['email', 'username', 'password', 'role']
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        role = attrs.get('role', '')
        # profile_picture = attrs.get('profile_picture', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'role']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'profile_picture', 'bio']
