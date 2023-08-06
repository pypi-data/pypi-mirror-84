from functools import wraps
from flask import request
import decimal
import json


def with_page(model):
    def decorated(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = {model.partition_key: request.args.get(model.partition_key)}
            if model.sort_key:
                key[model.sort_key] = request.args.get(model.sort_key)

            kwargs['last_key'] = key
            return f(*args, **kwargs)

        return wrapped

    return decorated


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        if isinstance(o, decimal.Decimal):
            value = float(o)
            if value.is_integer():
                return int(value)
            return value
        return super().default(o)
