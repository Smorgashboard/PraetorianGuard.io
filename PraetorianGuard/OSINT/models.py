from django.db import models

# Create your models here.

class OSINTS(models.Model):
    scan_id = models.CharField(max_length=24)
    scan_type = models.CharField(max_length=6, blank=True)
    company_name = models.CharField(max_length=32)
    target = models.CharField(max_length=64)
    scan_name = models.CharField(max_length=32)
    scan_date = models.DateField(auto_now_add=True)
    msp_id = models.CharField(max_length=32, default="msp_id")

class domainResults(models.Model):
    scan_id = models.CharField(max_length=24)
    company_name = models.CharField(max_length=32)
    target = models.CharField(max_length=64)
    scan_name = models.CharField(max_length=32)
    scan_date = models.DateField(auto_now_add=True)
    msp_id = models.CharField(max_length=32)
    pws = models.CharField(max_length=32)
    