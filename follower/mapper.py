from django.db import models
import feedparser
from datetime import datetime
import pytz,urllib
from models import Email
from django.conf import settings

feedparser.USER_AGENT='OSMFollower/1.0 +http://mapexplorer.org'

class Mapper(models.Model):
    user=models.CharField(max_length=99)
    scan_date=models.DateTimeField('last_scan_date',null=True,blank=True)
    edit_date=models.DateTimeField('edit_date',null=True,blank=True)
    first_edit_date=models.DateTimeField('first_edit_date',null=True,blank=True)
    min_edit_count=models.IntegerField('min_edit_count',null=True,blank=True)
    reach_outs=models.ManyToManyField(Email,through="ReachOut")

    def check_edits(self):
        url='http://' + settings.OSM_API + '/user/' \
            +urllib.quote(self.user) + '/edits/feed'
        feed=feedparser.parse(url)
        if feed.status != 200:
            return
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
            if self.min_edit_count == None or \
                    self.min_edit_count < len(feed.entries):
                self.min_edit_count=len(feed.entries)
            self.scan_date=datetime.now(pytz.utc)
