from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from cities_light.models import City, Country


class Contact(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    status = models.ForeignKey('ContactStatusChoices', on_delete=models.PROTECT, related_name='contacts')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.name} {self.surname}'


    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class ContactStatusChoices(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=30, unique=True)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Contact status choice'
        verbose_name_plural = 'Contact status choices'