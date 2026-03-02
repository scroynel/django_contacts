from django.contrib import admin
from .models import Contact, ContactStatusChoices
from .forms import ContactForm


# admin.site.register(Contact)
@admin.register(ContactStatusChoices)
class ContactStatusChoicesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactForm