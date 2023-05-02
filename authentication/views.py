from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import time
import hashlib
from django.contrib.auth import authenticate, login


from . import models

from cryptography.fernet import Fernet
# Create your views here.
import re

def index(request):
    return render(request,'auth/register.html')
def store(request):
    if(request.method=="POST"):
        
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pw = request.POST.get('pass')
        con_pw = request.POST.get('con_pass')
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        valid = 0
        if(re.fullmatch(regex,email)):
            valid = 1
        else:
            valid = 0

        if((len(uname)==0) or (len(email)==0) or (len(pw)==0) or (len(con_pw)==0)):
            return HttpResponse(" The field can not be empty")
        elif(pw!=con_pw):
            return HttpResponse("The password does not match")
        elif(valid == 0):
            return HttpResponse("The email is not valid")
        else:
            admin  = models.Admins()
            
            current_time = time.time()
            v_key = uname+str(current_time)
            # key = Fernet.generate_key()
            # fernet = Fernet(key)
            # encMessage = fernet.encrypt(v_key.encode())
            result = hashlib.md5(v_key.encode())
            result = result.hexdigest()
            v_status = 0
            admin.name = uname
            admin.email = email
            admin.password = pw
            admin.v_key = result
            admin.v_status = v_status
            admin.save()
            # decMessage = fernet.decrypt(encMessage).decode()
            link = "http://127.0.0.1:8000/register/verification/"+str(result)
            # print(link)
            msg = "Click this verification link"
            rendered = render_to_string('auth/reg_email.html', {'content': msg, 'link':link})
            text_content = strip_tags(rendered)
            email = EmailMultiAlternatives(
                "User Registration",
                text_content,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.attach_alternative(rendered,"text/html")
            email.send()
            return HttpResponse("success")
def verify(request, v_key):
    admin  = models.Admins()
    record = models.Admins.objects.get(v_key=v_key)
    record.v_status = 1
    # if(len(record)==1):
    record.save(update_fields=['v_status'])
    record = models.Admins.objects.get(v_key=v_key, v_status=1) 
    if(record):
        
        return HttpResponse("verification status updated")

def login(request):
    return render(request,'auth/login.html')

def login_auth(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        user = authenticate(request, email=email, password=password)
        #print("asdasda",user)
        if user:
            return HttpResponse("Login Success")
        else:
            return HttpResponse("login failed")

    #print("hello")
    
    # if(len(record)==1):

   
        
   

