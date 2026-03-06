from django.contrib import admin
from .models import Contact, ContactStatusChoices, GeoCache
from .forms import ContactForm



@admin.register(ContactStatusChoices)
class ContactStatusChoicesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'surname', 'email', 'phone', 'status', 'time_created']
    form = ContactForm
    
admin.site.register(GeoCache)