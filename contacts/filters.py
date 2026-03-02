import django_filters
from django.db.models import Q
from .models import Contact

class ContactFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_multiple_fields', label='Search')

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

    
    def filter_by_multiple_fields(self, queryset, name, value):
        """
        Filters queryset by multiple fields using OR logic.
        For example: search in name or surname.
        """
        return queryset.filter(
            Q(name__icontains=value) | Q(surname__icontains=value) | Q(city__icontains=value) | Q(status__name__icontains=value)
        )