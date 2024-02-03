from django.db import models

# Create your models here.
class Companies(models.Model):
    msp_id = models.CharField(max_length=32)
    company_name = models.CharField(max_length=32)
    public_ip = models.CharField(max_length=15, null=True)
    company_domain = models.CharField(max_length=64, null=True)
    primary_mail_domain = models.CharField(max_length=32)
    is_verified = models.BooleanField(default=False)
    company_id = models.CharField(max_length=10, null=True)
    verification = models.CharField(max_length=24, null=True)

    def __str__(self):
        return self.company_name