from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Permite acceder a un valor de diccionario usando una variable como clave en las plantillas de Django.
    Uso: {{ mi_diccionario|get_item:mi_clave }}
    """
    return dictionary.get(key) 