from datetime import datetime
import pytz
from django.db import models
import feedparser
feedparser.USER_AGENT='OSMFollower/1.0 +http://mapexplorer.org'

# Create your models here.
class Mapper(models.Model):
    user=models.CharField(max_length=20)
    scan_date=models.DateTimeField('last_scan_date',null=True,blank=True)
    edit_date=models.DateTimeField('last_edit_date',null=True,blank=True)
    first_edit_date=models.DateTimeField('last_edit_date',null=True,blank=True)
    def check_edits(self):
        feed=feedparser.parse('http://www.openstreetmap.org/user/'
                          + self.user + '/edits/feed')
        if len(feed.entries) > 0:
            published_parsed=feed.entries[0].published_parsed
            self.edit_date=datetime(published_parsed.tm_year
                                    ,published_parsed.tm_mon
                                    ,published_parsed.tm_mday
                                    ,published_parsed.tm_hour
                                    ,published_parsed.tm_min
                                    ,published_parsed.tm_sec
                                    ,0
                                    ,pytz.utc)
            published_parsed=feed.entries[-1].published_parsed
            first_edit_date=datetime(published_parsed.tm_year
                                     ,published_parsed.tm_mon
                                     ,published_parsed.tm_mday
                                     ,published_parsed.tm_hour
                                     ,published_parsed.tm_min
                                     ,published_parsed.tm_sec
                                     ,0
                                     ,pytz.utc)

            
            if self.first_edit_date==None or \
                    first_edit_date < self.first_edit_date:
                self.first_edit_date=first_edit_date
                
            self.scan_date=datetime.now(pytz.utc)

