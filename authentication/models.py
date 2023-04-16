from django.db import models

class Admins(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 500)
    email = models.EmailField(max_length = 500)
    password = models.CharField(max_length = 500)
    v_key = models.CharField(max_length = 500,default=0)
    v_status = models.CharField(max_length = 500, default=0)