from django.db import models

# Create your models here.

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.EmailField(max_length=45)
    password     = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=13)
    
    class Meta:
        db_table = 'users'
    