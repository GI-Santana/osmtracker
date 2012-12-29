# Create your views here.
from django.http import HttpResponse
from follower.mapper import Mapper
from follower.models import Email
from follower.reachout import ReachOut
from django.template import Context,RequestContext,loader
import datetime,pytz,time
from django.contrib.auth.decorators import login_required
import urllib2,urllib
import cookielib,StringIO,Cookie
import xml.etree.cElementTree as ElementTree
inptag = '{http://www.w3.org/1999/xhtml}input'
formtag = '{http://www.w3.org/1999/xhtml}form'

@login_required
def list(request):
    """
    Display a list of mappers we are following
    If the mapppers changeset RSS feed hasn't been scanned
    in the last 24h we scan it for updates
    """
    tracker_list=Mapper.objects.all().order_by('-edit_date')
    yesterday=datetime.datetime.now()-datetime.timedelta(days=1)    
    for mapper in tracker_list:
        if mapper.scan_date==None or  \
        mapper.scan_date.utctimetuple() < yesterday.utctimetuple():
            mapper.check_edits()
            mapper.save()
            #sleep for 10 seconds after checking the
            #RSS feed. We don't want to overload OSM
            time.sleep(3)
    t=loader.get_template('follower/list.html')
    c=Context({'tracker_list':tracker_list})
    
    return HttpResponse(t.render(c))

@login_required
def mapper_bulk_action(request):
    """
    Perform a bulk action to a list of mappers.
    This view is for dispatching bulk actions on a list of mappers
    """
    print request
    if request.GET.has_key('action') and request.GET['action']=='reach out':
        return reach_out(request)


@login_required
def reach_out(request):
    """
    Create a mapper reach out to a list of mappers.
    """
    tracker_list=Mapper.objects.all()
    selected=[]
    for mapper in tracker_list:
            key='mapper_selected_' + str(mapper.id)
            if request.GET.has_key(key) and request.GET[key]=='on':
                selected.append(mapper)

    emails=Email.objects.all()
    
    t=loader.get_template('follower/reach_out.html')
    
    c=RequestContext(request,{'mappers': selected,
               'emails' : emails })
    return HttpResponse(t.render(c))

@login_required
def reach_out_create(request):
    """
    Create a mapper reach out in response to the requested actions
    """
    print request
    email=None
    if request.POST.has_key('email'):
        email_id=request.POST['email']
        email = Email.objects.filter(id=email_id)
    count=0
    if request.POST.has_key('mapper_count'):
        count=int(request.POST['mapper_count'])
    cookies = authenticate_osm(request.POST['osm_user'],
                                       request.POST['osm_password'])
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    sent=[]
    failed=[]

    for idx in range(0,count):
        if request.POST.has_key('mapper_'+str(idx)):
            mapper_id=request.POST['mapper_'+str(idx)]
            mapper = Mapper.objects.filter(id=mapper_id)
            reach = ReachOut(email=email[0]
                             ,contact_date=datetime.datetime.now()
                             ,mapper=mapper[0])
            try:           
                reach.sendMessage(opener,cookies)
                reach.save()
                sent.append(reach)
            except ReachOut.SendException,e:
                failed.append(e)
            
    t=loader.get_template('follower/reach_out_sent.html')
    
    c=RequestContext(request,{'sent': sent,
               'failed' : failed })
    return HttpResponse(t.render(c))


def authenticate_osm(username,password):
    """
    establishes a client connection with OSM and authenticates against the API
    This method will return a set of cookies in a CookieJar usable to identify
    the session in future calls
    
    """

    login_payload={}

    request=urllib2.Request('http://api06.dev.openstreetmap.org/login')
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    response_tokenfetch = opener.open(request)
    html = response_tokenfetch.read()
    htmlfile=StringIO.StringIO(html)
    
    xml_tree = ElementTree.parse(htmlfile)
    for form in xml_tree.getiterator(formtag):                
        for field in form.getiterator(inptag):
            if 'name' in field.attrib and 'value' in field.attrib:
                login_payload[field.attrib['name']] = field.attrib['value']
    login_payload['username'] = username
    login_payload['password'] = password
    for field in login_payload:
        login_payload[field]=login_payload[field].encode('utf-8')
        #print("%s : %s " % (field, login_payload[field]))

    #cookies.extract_cookies(response_tokenfetch,request)
    print cookies
    cookies.add_cookie_header(request)
    response = opener.open(request,urllib.urlencode(login_payload))
    print response.info()
    print response.geturl()
    #cookies.extract_cookies(response,request)  
    
    return cookies

