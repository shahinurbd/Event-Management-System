from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def humanized_date(value):
    if value:
        today = datetime.now().date()
        value = timezone.localtime(value)

        if value.date() == today:
            return f"Today at {value.strftime('%I:%H %p')}"
        if value.date() == today.replace(day=today.day - 1):
            return f"Yesterday at {value.strftime('%I:%H %p')}"
        else:
            return f"{value.date().strftime('%B %d')}, {value.strftime('%I:%H %p')}"
        
    else:
        return f"No login record available"