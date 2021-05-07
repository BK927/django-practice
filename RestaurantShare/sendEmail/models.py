from django.db import models

# Create your models here.
class SMTP_Account(models.Model):
  user_name = models.CharField(max_length=256)
  password = models.CharField(max_length=256)