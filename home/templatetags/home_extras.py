# home/templatetags/home_extras.py
from django import template
from django.utils.text import Truncator
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def truncatewords_rtl(value, num):
    """
    Truncate to 'num' words and prepend an ellipsis for RTL text.
    """
    try:
        length = int(num)
    except (ValueError, TypeError):
        return value  # invalid argument

    # Split on whitespace to get words
    words = str(value).split()
    if len(words) <= length:
        return value  # no truncation needed

    # Take first 'length' words
    truncated = " ".join(words[:length])
    # Prepend ellipsis + space so it sits on the left in RTL
    return mark_safe(f"… {truncated}")