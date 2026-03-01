from django.contrib import admin
from .models import Contact, ContactStatusChoices
from .forms import ContactForm


# admin.site.register(Contact)
admin.site.register(ContactStatusChoices)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactForm