import base64
import datetime
import json
from decimal import Decimal
from uuid import UUID

try:
    from django.db.models import DjangoModel
    from django.core.files.uploadedfile import UploadedFile

    django_installed = True
except ImportError:
    DjangoModel = None
    DjangoUploadedFile = None
    django_installed = False


class APIJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (UUID, Decimal)):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        elif django_installed and isinstance(obj, DjangoModel):
            return obj.id
        elif django_installed and isinstance(obj, DjangoUploadedFile):
            position = obj.tell()
            obj.seek(0)
            res = base64.b64encode(obj.read()).decode("ascii")
            obj.seek(position)
            return res
        else:
            return super().default(obj)
