from rest_framework import viewsets
from .models import Contact
from .serializers import ContactAllSerializer, ContactPartSerializer


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('-time_created')


    def get_serializer_class(self):
        if self.action == 'list':
            return ContactPartSerializer
        return ContactAllSerializer