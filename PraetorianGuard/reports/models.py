from django.db import models
from jobsa.models import Job

# Create your models here.
class Report(models.Model):
    #job_id = models.ForeignKey(Job, related_name='job_id', on_delete=models.DO_NOTHING)
    clicked = models.BooleanField(default=False)
    #email_address = models.ForeignKey(Job, related_name='email_address', on_delete=models.DO_NOTHING)