from django.db import models

# Create your models here.

class Email(models.Model):
    """
    The email class is a an email template that can be
    sent to mappers.
    """
    text=models.TextField()
    subject=models.CharField(max_length=50)


