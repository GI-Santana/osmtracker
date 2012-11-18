# Create your views here.
from django.http import HttpResponse
from follower.models import Mapper
from django.template import Context,loader
import datetime,pytz,time

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

