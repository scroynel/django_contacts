from rest_framework import serializers
from .models import Contact, ContactStatusChoices


class ContactPartSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(slug_field='name', queryset=ContactStatusChoices.objects.all())
    time_created = serializers.DateTimeField(format='%d.%m.%Y - %H:%M', read_only=True)
    
    class Meta:
        model = Contact
        fields = ['id', 'name', 'surname', 'phone', 'email', 'city', 'status', 'time_created']
        extra_kwargs = {
            'phone': {'write_only': True},
            'email': {'write_only': True}
        }


class ContactAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'