from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Contact


def contacts(request):
    return render(request, template_name='contacts/contacts.html') 


class ContactListView(ListView):
    queryset = Contact.objects.all()
    template_name = 'contacts/contacts.html'
    context_object_name = 'contacts'