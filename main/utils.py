import uuid
from datetime import date, datetime
import slackweb

from django.db import models
from django.contrib import admin
from django.conf import settings

slack = slackweb.Slack(url=settings.SLACK_WEBHOOK_URL)


def get_field_names(cls):
    return [f.name for f in cls._meta.fields]


def model_to_dict(obj):
    res = {}
    for field in obj._meta.fields:
        name = field.name
        item = getattr(obj, name)
        if issubclass(type(item), models.Model):
            res[name] = model_to_dict(item)
        else:
            res[name] = item
    for field in obj._meta.many_to_many:
        name = field.name
        res[name] = []
        for item in getattr(obj, name).all():
            res[name].append(model_to_dict(item))
    return res


def create_admin(cls):
    return type("%sAdmin" % cls.__name__, (admin.ModelAdmin, ),
                {"list_display": get_field_names(cls)})


def register_admin(cls):
    admin.site.register(cls, create_admin(cls))


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, (uuid.UUID)):
        return str(obj)
    raise TypeError("Type %s not serializable" % type(obj))


def slack_notify(text):
    try:
        slack.notify(text=text)
    except Exception as e:
        print(e)
