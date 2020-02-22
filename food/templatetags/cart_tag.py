from django import template
from django.conf import settings
from food.models import *

# register = template.Library()

# @register.filter
# def cart_total(user):
#     order = Order.objects.filter(user=user, ordered=False)

#     if order.exists():
#     	return order[0].orderitems.count()
#     else:
#     	return 0


register = template.Library()

@register.simple_tag
def cart_total():
  return Cart.objects.count()

# @register.filter(name='total_item_tot') 
@register.simple_tag
def total_item_tot():
  cardd=Cart.objects.all()
  return cardd

@register.simple_tag
def cash_total():
  total=Order.objects.filter( ordered=False)
  t=total[0].get_totals()
  return t

@register.simple_tag
def tex_total():
  total=Order.objects.filter( ordered=False)
  t=total[0].get_percentage()
  return t

@register.simple_tag
def all_total_cash():
  total=Order.objects.filter( ordered=False)
  t=total[0].all_total()
  return t