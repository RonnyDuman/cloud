from django import template

register = template.Library()

@register.filter
def floatval(value):
    try:
        return float(value)
    except:
        return 0.0

@register.filter
def descontar(precio, descuento):
    try:
        return round(float(precio) * (1 - float(descuento)/100), 2)
    except:
        return precio

@register.filter
def dictkey(diccionario, clave):
    return diccionario.get(clave)
