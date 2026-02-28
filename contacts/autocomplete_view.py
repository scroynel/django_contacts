from dal import autocomplete
from cities_light.models import City

class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all().order_by('name')

        # Filter by country if provided
        country_id = self.forwarded.get('country', None)
        if country_id:
            qs = qs.filter(country_id=country_id)

        # Optional: filter by search query (typed by user)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs