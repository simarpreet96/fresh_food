from django import template
from django.conf import settings
from blog.models import Post

register = template.Library()

@register.simple_tag
def my_count():
   return Post.objects.count()
