from django.contrib.auth.backends import ModelBackend
from authentication.models import Admins

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
                #orm
            user = Admins.objects.get(email=email, v_status=1, password=password)
            print("hello",user)
            return user
            # if user.check_password(password):
                
            # return user


        #if user.check_password(password):
            #return user

        