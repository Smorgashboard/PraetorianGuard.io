from django.db import models

# Create your models here.

class Scans(models.Model):
    scan_id = models.CharField(max_length=24)
    company_name = models.CharField(max_length=32)
    target = models.CharField(max_length=64)
    scan_name = models.CharField(max_length=32)
    scan_date = models.DateField(auto_now_add=True)
    file_name = models.CharField(max_length=1024, blank=True)
    completed = models.BooleanField(default=False)
    msp_id = models.CharField(max_length=32, default="msp_id")
    sum_line = models.CharField(max_length=14000, blank=True)
    sum = models.CharField(max_length=14000, blank=True)
    alerts = models.CharField(max_length=14000, blank=True)
    resu = models.CharField(max_length=14000, blank=True)
    warns = models.CharField(max_length=14000, blank=True)
    info = models.CharField(max_length=14000, blank=True)
    errors = models.CharField(max_length=14000, blank=True)
    finds = models.CharField(max_length=14000, blank=True)
    vulns = models.CharField(max_length=14000, blank=True)
