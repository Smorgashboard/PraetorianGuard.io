from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class EmailTracking(models.Model):
    msp_id = models.CharField(max_length=32)
    company_name = models.CharField(max_length=32)
    campaign_name = models.CharField(max_length=32)
    campaign_id = models.CharField(max_length=32)
    tracking_id = models.CharField(max_length=16)
    email_clicked = models.BooleanField(default=False)
    email_clicked_time = models.TimeField()
    link_clicked = models.BooleanField(default=False)
    link_clicked_time = models.TimeField()
    target_email = models.CharField(max_length=128)
    template_name = models.CharField(max_length=32)

    
class Campaigns(models.Model):
    date = models.DateField(auto_now=True)
    msp_id = models.CharField(max_length=32)
    company_name = models.CharField(max_length=32)
    campaign_name = models.CharField(max_length=32)
    campaign_id = models.CharField(max_length=32)
    template_name = models.CharField(max_length=32)
    hidden = models.BooleanField(default=False)
    email_1 = models.EmailField(max_length=100)
    email_2 = models.EmailField(max_length=100)
    email_3 = models.EmailField(max_length=100)
    email_4 = models.EmailField(max_length=100)
    email_5 = models.EmailField(max_length=100)
    email_6 = models.EmailField(max_length=100)
    email_7 = models.EmailField(max_length=100)
    email_8 = models.EmailField(max_length=100)
    email_9 = models.EmailField(max_length=100)
    email_10 = models.EmailField(max_length=100)
    email_11 = models.EmailField(max_length=100)
    email_12 = models.EmailField(max_length=100)
    email_13 = models.EmailField(max_length=100)
    email_14 = models.EmailField(max_length=100)
    email_15 = models.EmailField(max_length=100)
    email_16 = models.EmailField(max_length=100)
    email_17 = models.EmailField(max_length=100)
    email_18 = models.EmailField(max_length=100)
    email_19 = models.EmailField(max_length=100)
    email_20 = models.EmailField(max_length=100)
    email_21 = models.EmailField(max_length=100)
    email_22 = models.EmailField(max_length=100)
    email_23 = models.EmailField(max_length=100)
    email_24 = models.EmailField(max_length=100)
    email_25 = models.EmailField(max_length=100)
    email_26 = models.EmailField(max_length=100)
    email_27 = models.EmailField(max_length=100)
    email_28 = models.EmailField(max_length=100)
    email_29 = models.EmailField(max_length=100)
    email_30 = models.EmailField(max_length=100)