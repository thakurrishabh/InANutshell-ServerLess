from django import template
register = template.Library()

@register.filter
def get_user(indexable):
    
    rs=indexable.split('@')[0]
    rp=rs.replace(".", "_")
    return rp