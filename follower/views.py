# Create your views here.
from django.http import HttpResponse
from follower.models import Mapper
from follower.models import Email
from follower.models import ReachOut
from django.template import Context,RequestContext,loader
import datetime,pytz,time
from django.contrib.auth.decorators import login_required

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
    if request.POST.has_key('email'):
        email_id=request.POST['email']
        email = Email.objects.filter(id=email_id)
    count=0
    if request.POST.has_key('mapper_count'):
        count=int(request.POST['mapper_count'])
    for idx in range(0,count):
        if request.POST.has_key('mapper_'+str(idx)):
            mapper_id=request.POST['mapper_'+str(idx)]
            mapper = Mapper.objects.filter(id=mapper_id)
            reach = ReachOut(email=email[0]
                             ,contact_date=datetime.datetime.now()
                             ,mapper=mapper[0])
            #send the email.
            reach.save()
            print "saved"
    
    return HttpResponse('')
