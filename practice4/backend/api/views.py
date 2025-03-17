from rest_framework import viewsets, generics
from .models import Item
from .serializers import ItemSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer