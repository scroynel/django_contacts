from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView
from .models import Contact
from .forms import ContactForm


class MyLoginView(LoginView):
    template_name = 'contacts/registration/login.html'


class ContactListView(ListView):
    model = Contact
    template_name = 'contacts/contacts.html'
    context_object_name = 'contacts'

    allowed_sort_fields = ['last_name', '-last_name', 'created_at', '-created_at']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     sort = self.request.GET.get('sort')

    #     if sort in self.allowed_sort_fields:
    #         queryset = queryset


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
    
    

