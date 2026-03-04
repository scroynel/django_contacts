from django.urls import reverse_lazy
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django_filters.views import FilterView
from .models import Contact, ContactStatusChoices
from .forms import ContactForm, ContactCSVForm
from .filters import ContactFilter
import io
import csv
import os
import requests


class MyLoginView(LoginView):
    template_name = 'contacts/registration/login.html'


class ContactListView(FilterView):
    model = Contact
    filterset_class = ContactFilter
    template_name = 'contacts/contacts.html'
    context_object_name = 'contacts'


    def get_queryset(self):
        return Contact.objects.select_related('status').all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload_form'] = ContactCSVForm()

        weather_data = {}

        # Get cities of contacts without dublicates
        contacts = set([item['city'] for item in self.get_queryset().values('city')])

        headers = {'User-Agent': 'MyGeocodingApp/1.0'}

        # for city in contacts:
        #     geo_api_key = f'https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1'

        #     response_geo = requests.get(geo_api_key, headers=headers)
        #     if response_geo.status_code == 200:

        #         lat = response_geo.json()[0]['lat']
        #         lon = response_geo.json()[0]['lon']
            
        #         weather_api_key = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
        #         response_weather = requests.get(weather_api_key, headers=headers)
            
        #         if response_weather.status_code == 200:
        #             data = response_weather.json()   
        #             units = data['current_weather_units']
        #             values = data['current_weather']
        #             weather = {key: f'{val} {units[key]}' for key, val in values.items()}
                    
        #             weather_data[city] = {
        #                 'temperature': weather['temperature'],
        #                 'windspeed': weather['windspeed']
        #             }
        #             print(weather_data)
        #         else:
        #             print('Bad', response_weather.status_code)
        #     else:
        #             print('Bad', response_geo.status_code)
        # context['weather'] = weather_data

        return context
    

    def post(self, request, *args, **kwargs):
        form = ContactCSVForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES['file']

            status_map = {s.name.lower(): s for s in ContactStatusChoices.objects.all()}

            # Get existing phone numbers to avoid duplicates
            existing_phones = set(Contact.objects.values_list('phone', flat=True))

            # Get existing phone numbers to avoid duplicates
            existing_emails = set(Contact.objects.values_list('email', flat=True))

            with io.TextIOWrapper(uploaded_file, encoding='utf-8') as text_file:
                reader = csv.DictReader(text_file)

                contacts = []
                for row in reader:
                    try:
                        phone = row['phone'].strip()
                        email = row['email'].strip()

                        if phone in existing_phones or email in existing_emails:
                            continue

                        # Map CSV status to FK instance, fallback to None
                        status_instance = status_map.get(row['status'].strip().lower())

                        contact = Contact(
                            name = row['name'].strip(),
                            surname = row['surname'].strip(),
                            phone = phone,
                            email = email,
                            city = row['city'].strip(),
                            status=status_instance
                        )
                        contacts.append(contact)
                    except Exception:
                        # Skip invalid rows
                        continue

            with transaction.atomic():
                Contact.objects.bulk_create(contacts)
                

            return redirect(reverse_lazy('contacts'))
        return render(request, self.template_name, {'upload_form': form})






class ContactCreateView(CreateView):
    model = Contact
    template_name = 'contacts/create_contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')


class ContactUpdateView(UpdateView):
    model = Contact
    template_name = 'contacts/update_contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'contacts/delete_contact.html'
    success_url = reverse_lazy('contacts')
    
    

