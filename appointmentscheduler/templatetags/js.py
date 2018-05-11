from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
import json

register = template.Library()

@register.filter
def js(obj):
    return mark_safe(json.dumps(obj))