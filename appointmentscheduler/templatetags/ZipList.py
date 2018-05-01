from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

register = template.Library()

@register.filter(name='ZipList')
def zip_lists(a, b):
  return zip(a, b)