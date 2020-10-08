from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


def validate_date(date):
    if date < timezone.now().date():
        raise ValidationError("Date cannot be in the past")
    return date


def validate_time(time,date):
    today = datetime.datetime.now()
    if time < timezone.now().time() and date == today:
        raise ValidationError("Time cannot be past")
