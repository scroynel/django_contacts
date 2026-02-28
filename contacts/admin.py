from django.contrib import admin
from .models import Contact, ContactStatusChoices
from cities_light.models import City
from .forms import ContactAdminForm


# admin.site.register(Contact)
admin.site.register(ContactStatusChoices)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactAdminForm