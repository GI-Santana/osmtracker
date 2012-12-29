from datetime import datetime
import pytz
from django.db import models
import feedparser
import urllib,urllib2
import cookielib,StringIO,Cookie
import xml.etree.cElementTree as ElementTree

feedparser.USER_AGENT='OSMFollower/1.0 +http://mapexplorer.org'
inptag = '{http://www.w3.org/1999/xhtml}input'
formtag = '{http://www.w3.org/1999/xhtml}form'

# Create your models here.

class Email(models.Model):
    text=models.TextField()
    subject=models.CharField(max_length=50)

class Mapper(models.Model):
    user=models.CharField(max_length=99)
    scan_date=models.DateTimeField('last_scan_date',null=True,blank=True)
    edit_date=models.DateTimeField('last_edit_date',null=True,blank=True)
    first_edit_date=models.DateTimeField('last_edit_date',null=True,blank=True)
    min_edit_count=models.IntegerField('min_edit_count',null=True,blank=True)
    reach_outs=models.ManyToManyField(Email,through="ReachOut")

    def check_edits(self):
        url='http://www.openstreetmap.org/user/' \
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


    
class ReachOut(models.Model):
    mapper=models.ForeignKey(Mapper)
    email=models.ForeignKey(Email)
    contact_date=models.DateField()
    responsed=models.BooleanField()
    response=models.TextField(null=True,blank=True)
    class SendException(Exception):
        reason=None
        code=None
        mapper=None
        def __init__(self,reason,code,mapper):
            self.reason=reason
            self.code=code
            self.mapper=mapper

    def sendMessage(self,opener,cookies):
        
        payload = {}
        send_url = "http://api06.dev.openstreetmap.org/message/new/%s" % self.mapper.user
        request_getform=urllib2.Request(send_url)
        cookies.add_cookie_header(request_getform)
        try:
            response_send = opener.open(request_getform)
            html = response_send.read()
            htmlfile=StringIO.StringIO(html)
        
            xml_tree = ElementTree.parse(htmlfile)
            has_title=False
            for form in xml_tree.getiterator(formtag):                
                for field in form.getiterator(inptag):
                    if field.attrib['name'] == 'message[title]':
                        has_title=True
                    if 'name' in field.attrib and 'value' in field.attrib:
                            payload[field.attrib['name']] = field.attrib['value']
            if has_title==True:
                payload['message[title]']=self.email.subject
                payload['message[body]']=self.email.text
                for field in payload:
                    payload[field]=payload[field].encode('utf-8')
                request_send = urllib2.Request(send_url)
                cookies.add_cookie_header(request_send)
                print cookies
                print send_url
                response_send = opener.open(request_send,
                                            urllib.urlencode(payload))
            else:
                raise ReachOut.SendException(mapper=self.mapper
                                        ,reason='message[title] not found'
                                        ,code=0)
        except urllib2.HTTPError,e:
            raise ReachOut.SendException(mapper=self.mapper
                                ,reason='http error'
                                ,code=e.code)

