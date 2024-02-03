from django.db import models
from msps.models import MSP
from datetime import datetime

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    msp = models.ForeignKey(MSP, on_delete=models.DO_NOTHING)
    website_url = models.CharField(max_length=75)
    external_ip = models.CharField(max_length=15)
    primary_mail_domain = models.CharField(max_length=32)
    company_logo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.company_name
