from django.shortcuts import render


def contacts(request):
    return render(request, template_name='contacts/contacts.html') 