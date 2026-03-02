import django_filters
from .models import Contact

class ContactFilter(django_filters.FilterSet):

    ordering = django_filters.OrderingFilter(
        # tuple: (model_field, parameter_name)
        choices = (
            ('name', 'Name ↑'),
            ('-name', 'Name ↓'),
            ('surname', 'Surname ↑'),
            ('-surname', 'Surname ↓'),
            ('time_created', 'Date ↑'),
            ('-time_created', 'Date ↓'),
        )
    )

    class Meta:
        model = Contact
        fields = []