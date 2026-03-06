from django.urls import reverse_lazy
from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.views import LoginView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Contact, ContactStatusChoices, GeoCache
from .forms import ContactForm, ContactCSVForm
from .filters import ContactFilter
import io
import csv
import requests
from .utils import fetch_coords_background


class MyLoginView(LoginView):
    template_name = 'contacts/registration/login.html'


class ContactListView(LoginRequiredMixin, FilterView):
    model = Contact
    filterset_class = ContactFilter
    template_name = 'contacts/contacts.html'
    context_object_name = 'contacts'


    def get_queryset(self):
        return Contact.objects.select_related('status').filter(owner=self.request.user)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload_form'] = ContactCSVForm()
        
        if self.get_queryset().count():
            # Get cities of contacts with coords
            coords = GeoCache.objects.values_list('city_name', 'lat', 'lon')

            cities = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            lons = [c[2] for c in coords]

            lats_string = ','.join(map(str, lats))
            lons_string = ','.join(map(str, lons))
            
            headers = {'User-Agent': 'MyGeocodingApp/1.0'}
                
            weather_api_key = f'https://api.open-meteo.com/v1/forecast?latitude={lats_string}&longitude={lons_string}&current_weather=true'
            response_weather = requests.get(weather_api_key, headers=headers)
            data = response_weather.json()

            if isinstance(data, dict):
                data = [data]

            weather = []

            for item in data:
                units = item['current_weather_units']
                values = item['current_weather']
                weather.append({key: f'{val} {units[key]}' for key, val in values.items()})
            
            weather_cities = {
                    city:{
                    'temp': item['temperature'],
                    'wind': item['windspeed']
                }
                for city, item in zip(cities, weather)
            }

            context['weather_cities'] = weather_cities

        return context
    

    def post(self, request, *args, **kwargs):
        """Adding CVS files to database"""
        form = ContactCSVForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES['file']
            if not uploaded_file:
                return self.render_to_response(self.get_context_data(form=form, error="Файл не выбран"))

            status_map = {s.name.lower(): s for s in ContactStatusChoices.objects.all()}

            # Get existing phone numbers to avoid duplicates
            existing_phones = set(Contact.objects.values_list('phone', flat=True))

            # Get existing phone numbers to avoid duplicates
            existing_emails = set(Contact.objects.values_list('email', flat=True))
            contacts = []

            with io.TextIOWrapper(uploaded_file, encoding='utf-8') as text_file:
                reader = csv.DictReader(text_file)

                
                for row in reader:
                    try:
                        phone = row['phone'].strip()
                        email = row['email'].strip()

                        if phone in existing_phones or email in existing_emails:
                            continue

                        # Map CSV status
                        status_instance = status_map.get(row['status'].strip().lower())

                        contact = Contact(
                            name = row['name'].strip(),
                            surname = row['surname'].strip(),
                            phone = phone,
                            email = email,
                            city = row['city'].strip(),
                            status=status_instance,
                            owner=request.user
                        )
                        contacts.append(contact)
                    except Exception:
                        # Skip invalid rows
                        continue

            # 
            with transaction.atomic():
                Contact.objects.bulk_create(contacts)
                
            unique_cities = {c.city.strip() for c in contacts if c.city}

            # loop unique cities 
            for city_name in unique_cities:
                # Check if they are in our database
                if not GeoCache.objects.filter(city_name=city_name).exists():
                    fetch_coords_background(city_name)

            
        return redirect(reverse_lazy('contacts'))


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = 'contacts/create_contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')


    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        city_name = self.object.city 
        fetch_coords_background(city_name)
        return response


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'contacts/create_contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)
    

    def form_valid(self, form):
        old_city = self.get_object().city
        new_city = form.cleaned_data.get('city')

        response = super().form_valid(form)

        if new_city and new_city != old_city:
            fetch_coords_background(new_city)

        return response

    
class AjaxDeleteView(LoginRequiredMixin, SingleObjectMixin, View):
    """
    Works like DeleteView, but without confirmation screens or a success_url.
    """
    model = Contact


    def get_object(self, queryset = None):
        return get_object_or_404(Contact, pk=self.kwargs['pk'])


    def post(self, *args, **kwargs):
        is_ajax = self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            if self.request.method == 'POST':
                self.object = self.get_object()
                self.object.delete()
                
                return JsonResponse({'status': 1})
            return JsonResponse({'status': 'Invalid request'}, status=400)
        else:
            return HttpResponseBadRequest('Invalid request')