import uuid
from datetime import date, datetime, timedelta
import slackweb
import numpy as np
import pickle

from django.db import models
from django.contrib import admin
from django.conf import settings
from django.utils import timezone

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
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError("Type %s not serializable" % type(obj))


def slack_notify(text):
    try:
        slack.notify(text=text)
    except Exception as e:
        print(e)


def get_next_minute_datetime(d):
    return timezone.localtime(d + timedelta(minutes=1) - timedelta(
        seconds=d.second) - timedelta(microseconds=d.microsecond))


def get_prev_minute_datetime(d):
    return timezone.localtime(d - timedelta(seconds=d.second) -
                              timedelta(microseconds=d.microsecond))


class MacOSFile(object):
    def __init__(self, f):
        self.f = f

    def __getattr__(self, item):
        return getattr(self.f, item)

    def read(self, n):
        # print("reading total_bytes=%s" % n, flush=True)
        if n >= (1 << 31):
            buffer = bytearray(n)
            idx = 0
            while idx < n:
                batch_size = min(n - idx, 1 << 31 - 1)
                # print("reading bytes [%s,%s)..." % (idx, idx + batch_size), end="", flush=True)
                buffer[idx:idx + batch_size] = self.f.read(batch_size)
                # print("done.", flush=True)
                idx += batch_size
            return buffer
        return self.f.read(n)

    def write(self, buffer):
        n = len(buffer)
        print("writing total_bytes=%s..." % n, flush=True)
        idx = 0
        while idx < n:
            batch_size = min(n - idx, 1 << 31 - 1)
            print(
                "writing bytes [%s, %s)... " % (idx, idx + batch_size),
                end="",
                flush=True)
            self.f.write(buffer[idx:idx + batch_size])
            print("done.", flush=True)
            idx += batch_size


def pickle_dump(obj, file_path):
    with open(file_path, "wb") as f:
        return pickle.dump(obj, MacOSFile(f), protocol=pickle.HIGHEST_PROTOCOL)


def pickle_load(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(MacOSFile(f))
