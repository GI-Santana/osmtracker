from django.db import models
from follower.mapper import Mapper
from follower.models import Email

import urllib,urllib2
import cookielib,StringIO,Cookie
import xml.etree.cElementTree as ElementTree

inptag = '{http://www.w3.org/1999/xhtml}input'
formtag = '{http://www.w3.org/1999/xhtml}form'

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

