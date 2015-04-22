from django.shortcuts import render_to_response, get_object_or_404, redirect
from extension.models import Opportunity, Association
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from google.appengine.api import users


def associate(request, thread_id):
  if not users.get_current_user():
    return HttpResponseRedirect(users.create_login_url(request.path))

  if request.method == "GET":
    print 'HEHEHE'
    variables = {}
    if Association.objects.filter(thread_id=thread_id).count() > 0:
      return render_to_response("extension/already_associated.html", variables, context_instance=RequestContext(request))
    print Association.objects.filter(thread_id=thread_id).count()
    opps = Opportunity.objects.all()
    variables['opps'] = opps

    return render_to_response("extension/associate.html", variables, context_instance=RequestContext(request))
  else:
    variables = {}
    curr_opp = Opportunity.objects.get(pk=request.POST['opp'])
    print curr_opp
    association = Association() 
    association.thread_id = thread_id
    association.email_id = "" #TODO
    association.opportunity = curr_opp
    association.created_user = users.get_current_user()
    association.save()

    return redirect("/extension/thanks")

def thanks(request):
  return  render_to_response("extension/thanks.html")