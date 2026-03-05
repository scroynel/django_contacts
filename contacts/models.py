from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    surname = models.CharField(max_length=50, db_index=True)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=50, db_index=True)
    status = models.ForeignKey('ContactStatusChoices', on_delete=models.PROTECT, related_name='contacts')
    time_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class ContactStatusChoices(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    code = models.CharField(max_length=30, unique=True)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Contact status choice'
        verbose_name_plural = 'Contact status choices'


class GeoCache(models.Model):
    city_name = models.CharField(max_length=255, unique=True, db_index=True)
    lat = models.FloatField()
    lon = models.FloatField()


    def __str__(self):
        return self.city_name


    class Meta:
        verbose_name = 'Cache of coordinate'
        verbose_name_plural = 'Cache of coordinates'