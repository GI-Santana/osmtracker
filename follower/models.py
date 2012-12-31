from django.db import models
#from follower.reachout import ReachOut

# Create your models here.

class Email(models.Model):
    text=models.TextField()
    subject=models.CharField(max_length=50)
  
  #def is_sent(self):
  #      usages=ReachOut.objects.all().filter(email=self.id)
  #      return len(usages)>0
    

    
