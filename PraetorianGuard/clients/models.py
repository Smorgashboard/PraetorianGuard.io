from re import L
from telnetlib import DO
from django.db import models
from companies.models import Company

# Create your models here.
class Client(models.Model):
    client_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    company_name = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    client_first_name = models.CharField(max_length=100)
    client_last_name = models.CharField(max_length=100)