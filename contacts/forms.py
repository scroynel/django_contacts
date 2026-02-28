from django import forms
from dal import autocomplete
from .models import Contact

class ContactAdminForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'city': autocomplete.ModelSelect2(
                url='city-autocomplete',  # URL to autocomplete view
                forward=['country']       # forward the country field value
            )
        }