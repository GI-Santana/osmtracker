import datetime,pytz
from django.db import models
import feedparser
feedparser.USER_AGENT='OSMFollower/1.0 +http://mapexplorer.org'

# Create your models here.
class Mapper(models.Model):
    user=models.CharField(max_length=20)
    scan_date=models.DateTimeField('last_scan_date',null=True,blank=True)
    edit_date=models.DateTimeField('last_edit_date',null=True,blank=True)
    
    def check_edits(self):
        feed=feedparser.parse('http://www.openstreetmap.org/user/'
                          + self.user + '/edits/feed')
        self.edit_date=feed.entries[0].published
        self.scan_date=datetime.datetime.now(pytz.utc)

