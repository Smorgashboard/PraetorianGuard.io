from statistics import mode
from django.db import models

# Create your models here

class MSP(models.Model):
    msp_name = models.CharField(max_length=100)
    msp_logo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    contact_email = models.CharField(max_length=50)
    contact_first_name = models.CharField(max_length=50)
    contact_last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.msp_name