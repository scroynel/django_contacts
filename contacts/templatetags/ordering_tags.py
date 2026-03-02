from django import template
from urllib.parse import urlencode
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def ordering_link(context, field, label):
    """
    Generate a link with arrow.
    field - field's name of model.
    label - text, what you will see in the table
    """
    request = context['request']
    params = request.GET.copy()

    current = params.get('ordering')

    # Direction
    if current == field:
        direction = '-' + field
        arrow = '↑'
    elif current == '-' + field:
        direction = field
        arrow = '↓'
    else:
        direction = field
        arrow = ''

    params['ordering'] = direction
    url = '?' + urlencode(params)
    print(urlencode(params))

    return mark_safe(f'<a href="{url}">{label} {arrow}</a>')