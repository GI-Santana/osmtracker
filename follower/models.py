from django.db import models

# Create your models here.

class Email(models.Model):
    text=models.TextField()
    subject=models.CharField(max_length=50)



    
