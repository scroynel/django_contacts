from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            
        }


class ContactCSVForm(forms.Form):
    file = forms.FileField()


    def clean_file(self):
        file = self.cleaned_data['file']

        if not file.name.endswith('.csv'):
            raise forms.ValidationError('Only CSV files are allowed')

        max_size = 5 * 1024 * 1025 # 5MB
        if file.size > max_size:
            raise forms.ValidationError('File is large (max 5MB).')
        
        return file