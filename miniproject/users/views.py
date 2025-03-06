import base64
import logging

import pdfkit
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML

from users.forms import ProfileForm
from users.models import Profile
from users.serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, ProfileSerializer


def home_page(request):
    return render(request, 'users/home.html')
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self, request):
        return render(request, 'users/register.html')

    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def get(self, request):
        return render(request, 'users/login.html')

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

@login_required(login_url='/users/login/')
def profile_detail(request):
    profile = request.user.profile
    return render(request, 'users/profile_detail.html', {'profile': profile})

@login_required
def profile_update(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile_update.html', {'form': form})

@login_required
def profile_pdf(request):
    profile = request.user.profile

    if profile.profile_picture:
        try:
            with open(profile.profile_picture.path, "rb") as image_file:
                profile.profile_picture_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            profile.profile_picture_base64 = None
    else:
        profile.profile_picture_base64 = None

    html = render_to_string('users/profile_pdf.html', {'profile': profile})

    try:
        pdf = HTML(string=html).write_pdf()
    except Exception as e:
        raise

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{profile.user.username}_profile.pdf"'
    return response