from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Contact
from .serializers import ContactAllSerializer, ContactPartSerializer


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.select_related('status').all().order_by('-time_created')


    def get_serializer_class(self):
        if self.action == 'list':
            return ContactPartSerializer
        return ContactAllSerializer
    

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]