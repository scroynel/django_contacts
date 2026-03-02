from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView
from django_filters.views import FilterView
from .models import Contact
from .forms import ContactForm
from .filters import ContactFilter

class MyLoginView(LoginView):
    template_name = 'contacts/registration/login.html'


class ContactListView(FilterView):
    model = Contact
    filterset_class = ContactFilter
    template_name = 'contacts/contacts.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        return Contact.objects.all()


# class ContactListView(ListView):
#     model = Contact
#     template_name = 'contacts/contacts.html'
#     context_object_name = 'contacts'

#     allowed_sort_fields = ['name', '-time_created', ]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         sort = self.request.GET.get('sort')

#         if sort in self.allowed_sort_fields:
#             queryset = queryset.order_by(sort)

#         return queryset


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
    
    

