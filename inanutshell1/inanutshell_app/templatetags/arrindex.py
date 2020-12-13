from django import template
register = template.Library()

@register.filter
def arrindex(indexable, i):
    return indexable[:i]+" ..."