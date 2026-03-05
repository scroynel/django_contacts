from django.urls import reverse_lazy
from django.db import transaction
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.views import LoginView
from django_filters.views import FilterView
from .models import Contact, ContactStatusChoices, GeoCache
from .forms import ContactForm, ContactCSVForm
from .filters import ContactFilter
import io
import csv
import os
import requests
import threading
from .utils import fetch_coords_background


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

        # Get cities of contacts without dublicates
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
        print(data)

        weather = []

        for item in data:
            units = item['current_weather_units']
            values = item['current_weather']
            weather.append({key: f'{val} {units[key]}' for key, val in values.items()})
        
        print(weather)
        
        weather_cities = {
                city:{
                'temp': item['temperature'],
                'wind': item['windspeed']
            }
            for city, item in zip(cities, weather)
        }

        print(weather_cities)

        context['weather_cities'] = weather_cities
        # results = data['current_weather']
        # print(results)


        # if isinstance(results, dict):
        #     results = [results]

        # weather = {
        #     city:{
        #         'temp': item['temperature'],
        #         'wind': item['windspeed']
        #     }
        #     for city, item in zip(cities, results)
        # }

        # print(weather)

        
            


    
        # if response_weather.status_code == 200:
        #     data = response_weather.json()   
        #     units = data['current_weather_units']
        #     values = data['current_weather']
        #     weather = {key: f'{val} {units[key]}' for key, val in values.items()}
            
        #     weather_data[city] = {
        #         'temperature': weather['temperature'],
        #         'windspeed': weather['windspeed']
        #     }
        #     print(weather_data)
        # else:
        #     print('Bad', response_weather.status_code)
        

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
                
            unique_cities = {c.city.strip() for c in contacts if c.city}

            # 2. Обрабатываем города прямо здесь, в основном потоке
            for city_name in unique_cities:
                # Проверяем, есть ли город уже в кэше
                if not GeoCache.objects.filter(city_name=city_name).exists():
                    # Только если города нет, делаем паузу и запрос
                    # Это и есть та самая "таска", но выполняемая последовательно
                    fetch_coords_background(city_name)

            return redirect(reverse_lazy('contacts'))
        return render(request, self.template_name, {'upload_form': form})



class ContactCreateView(CreateView):
    model = Contact
    template_name = 'contacts/create_contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')

    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # 2. Запускаем фоновый поток, передаем название города
        # Пользователь не будет ждать 1.1 секунду
        city_name = self.object.city # Предполагаем, что в модели Contact есть поле city
        fetch_coords_background(city_name)
        
        return response


class ContactUpdateView(UpdateView):
    model = Contact
    template_name = 'contacts/update_contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'contacts/delete_contact.html'
    success_url = reverse_lazy('contacts')
    
    
class AjaxDeleteView(SingleObjectMixin, View):
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
                
                count = Contact.objects.all().count()
                print(count)
                # get block of code for empty cart
                # empty = render_to_string('partials/empty_cart.html')

                # return JsonResponse({'status': 1, 'count': count, 'empty_cart': empty})
                return JsonResponse({'status': 1, 'count': count,})
            return JsonResponse({'status': 'Invalid request'}, status=400)
        else:
            return HttpResponseBadRequest('Invalid request')