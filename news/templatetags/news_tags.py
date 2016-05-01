from django import template

from ..models import NewsPost


register = template.Library()


@register.simple_tag
def get_latest_posts(limit=5):
    return NewsPost.objects.all().order_by('-created')[:limit]
