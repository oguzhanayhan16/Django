from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend
from .models import Writer



class WriterBackend(BaseBackend):
    def authenticate(self, request, WriterMail=None, password=None, **kwargs):
        try:
            writer = Writer.objects.get(WriterMail=WriterMail)
            if writer.check_password(password):
                return writer
        except Writer.DoesNotExist:
            return None
        return None

    def get_user(self, writer_id):
        try:
            return Writer.objects.get(pk=writer_id)
        except Writer.DoesNotExist:
            return None