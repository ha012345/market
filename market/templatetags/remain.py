from django import template

register = template.Library()
@register.filter
def remain(value) :
    import datetime
    original_date_plus_24 = value + datetime.timedelta(hours=24)
    return original_date_plus_24
