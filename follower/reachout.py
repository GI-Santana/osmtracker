from django.db import models
from follower.mapper import Mapper
from follower.models import Email

import urllib,urllib2
import cookielib,StringIO,Cookie
import xml.etree.cElementTree as ElementTree
from django.conf import settings

inptag = '{http://www.w3.org/1999/xhtml}input'
formtag = '{http://www.w3.org/1999/xhtml}form'

class ReachOut(models.Model):
    """
    A ReachOut happens when we send an message(email) to a particular
    mapper.   The reachout is a many-to-many join class that connects
    mappers to emails.
    """
    mapper=models.ForeignKey(Mapper)
    email=models.ForeignKey(Email)
    contact_date=models.DateField()
    responsed=models.BooleanField()
    response=models.TextField(null=True,blank=True)

    
    class SendException(Exception):
        """ 
        An exception that is raised when an error sending the message occurs
        """
        reason=None
        code=None
        mapper=None
        def __init__(self,reason,code,mapper):
            self.reason=reason
            self.code=code
            self.mapper=mapper

    def sendMessage(self,opener,cookies):
        """
        Sends a message through through the OSM messaging API.

        opener - A urllib2 opener class

        cookies - a CookieJar object that contains the osm authentication
                  cookies.

        """
        payload = {}
        send_url = 'http://' + settings.OSM_API + "/message/new/%s" % self.mapper.user
        """
        send a GET request to the API to get the blank HTML form.
        We need to get this form to a hidden varaiable value that needs
        to be resubmitted in the POST request in order for the API/rails port
        to accept the message.
        
        
        """
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
                """
                Send the message as a POST.
                """
                response_send = opener.open(request_send,
                                            urllib.urlencode(payload))
            else:
                """
                The HTML form we fetched didn't look like we expected.
                Instead of blindly POSTing our data we will throw an error.
                """
                raise ReachOut.SendException(mapper=self.mapper
                                        ,reason='message[title] not found'
                                        ,code=0)
        except urllib2.HTTPError,e:
            raise ReachOut.SendException(mapper=self.mapper
                                ,reason='http error'
                                ,code=e.code)

