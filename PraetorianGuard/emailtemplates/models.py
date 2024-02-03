from django.db import models
from msps.models import MSP

# Create your models here.
class Emailtemplate(models.Model):
    msp_name = models.ForeignKey(MSP, on_delete=models.DO_NOTHING)
    email_teplate = models.TextField()

