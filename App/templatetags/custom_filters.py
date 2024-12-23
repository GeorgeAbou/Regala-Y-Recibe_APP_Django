from django import template

register = template.Library()

@register.filter
def to(value):
    """Convierte el valor a un número entero (rango)."""
    return range(value)