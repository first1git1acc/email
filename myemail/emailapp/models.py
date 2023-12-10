from django.db import models

# Create your models here.
class Mail(models.Model):
    email_to = models.CharField(max_length=64)
    mail = models.CharField(max_length=1000)
    mail_from = models.CharField(max_length=64)
    

