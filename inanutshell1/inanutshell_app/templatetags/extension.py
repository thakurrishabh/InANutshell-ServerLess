from django import template
register = template.Library()

@register.filter
def extension(indexable):
    return indexable[-3:]