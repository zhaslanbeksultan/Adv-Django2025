from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', profile_view, name="profile"),
    path('profile/pdf/', profile_pdf_view, name='profile_pdf'),
]