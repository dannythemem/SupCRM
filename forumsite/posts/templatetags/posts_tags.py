from django.utils import timezone

from django import template
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import datetime

register = template.Library()

@register.simple_tag(takes_context=True)
def time_ago(context, time_created):
    request = context.get('request')
    if not request:
        return ''
    tz = request.COOKIES.get('django_timezone')
    try:
        tz = ZoneInfo(tz) if tz else timezone.get_current_timezone()
    except ZoneInfoNotFoundError:
        tz = timezone.get_current_timezone()

    tz_time_created = time_created.astimezone(tz)
    tz_time_now = datetime.datetime.now(tz)
    delta = tz_time_now - tz_time_created
    total_seconds = delta.total_seconds()

    min = 60
    hour = 60 * min
    day = 24 * hour
    month = 30 * day
    year = 365 * day
    if total_seconds < 60:
        return 'Только что'
    if total_seconds < min:
        return f'{int(total_seconds)} с. назад'
    if total_seconds < hour:
        return f'{int(total_seconds // min)} мин. назад'
    if total_seconds < day:
        return f'{int(total_seconds // hour)} ч. назад'
    if total_seconds < month:
        return f'{int(total_seconds // day)} дн. назад'
    if total_seconds < year:
        return f'{int(total_seconds // month)} мес. назад'
    years = total_seconds // year
    return years

