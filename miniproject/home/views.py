from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from users.serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from django.contrib.auth import login

def home_page(request):
    return render(request, 'mysite/home.html')
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self, request):
        return render(request, 'mysite/register.html')

    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        # return redirect('login')
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
        return render(request, 'mysite/login.html')

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        # return redirect('home')
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # return redirect('login')