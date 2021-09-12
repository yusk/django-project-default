import re

from django.db import models


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


def get_by_manytomany(queryset, name, value, idx):
    m = list(re.finditer('_', name))
    i = m[idx].span()[0]
    model_name = f"{name[0:i]}s"
    key = name[i + 1:]
    kwargs = {f"{model_name}__{key}": value}
    return queryset.filter(**kwargs).distinct()
