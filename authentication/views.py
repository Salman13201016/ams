from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
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
            msg = "Click this verification link"
            rendered = render_to_string('auth/reg_email.html', {'content': msg})
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
        

        
        
   

