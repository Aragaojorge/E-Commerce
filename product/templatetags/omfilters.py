from django.template import Library
from utils import utils

register = Library()

@register.filter
def format_price(val):
    return utils.format_price(val)

@register.filter
def cart_total_qty(cart):
    return utils.cart_total_qty(cart)

@register.filter
def cart_totals(cart):
    return utils.cart_totals(cart)