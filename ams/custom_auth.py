from django.contrib.auth.backends import ModelBackend
from authentication.models import Admins

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        user = Admins.objects.get(email=email)
        if user.check_password(password) and user.status == 1:
            return user
        else:
            return None
    def get_user(self, user_id):
            return Admins.objects.get(pk=user_id)